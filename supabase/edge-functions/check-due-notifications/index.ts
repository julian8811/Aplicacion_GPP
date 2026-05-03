// supabase/functions/check-due-notifications/index.ts
// Cron function that runs daily to check for due action plans and evaluation schedules
// Schedule: Daily at 08:00 UTC

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"

const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY") || ""

interface DueNotification {
  user_id: string
  plans: Array<{
    title: string
    due_date: string
    status: string
  }>
}

interface ScheduleNotification {
  schedule_id: string
  user_id: string
  schedule_name: string
  due_date: string
}

// Convert due_date to a friendly format
function formatDate(dateStr: string): string {
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString("es-ES", { day: "numeric", month: "short", year: "numeric" })
  } catch {
    return dateStr
  }
}

// Determine status based on due_date
function getPlanStatus(dueDate: string): "pending" | "overdue" {
  const now = new Date()
  const due = new Date(dueDate)
  return due < now ? "overdue" : "pending"
}

// Calculate next due date based on frequency
function calculateNextDue(currentDue: string, frequency: string): string {
  const date = new Date(currentDue)
  
  switch (frequency) {
    case 'monthly':
      date.setMonth(date.getMonth() + 1)
      break
    case 'quarterly':
      date.setMonth(date.getMonth() + 3)
      break
    case 'biannual':
      date.setMonth(date.getMonth() + 6)
      break
    case 'annual':
      date.setFullYear(date.getFullYear() + 1)
      break
    default:
      date.setMonth(date.getMonth() + 3) // Default to quarterly
  }
  
  return date.toISOString()
}

async function queryDueNotifications(supabase: any): Promise<DueNotification[]> {
  const now = new Date()
  const sevenDaysFromNow = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000)

  // Query action plans that:
  // 1. Have a due_date within the next 7 days
  // 2. Haven't had a reminder sent yet
  const { data: plans, error } = await supabase
    .from("action_plans")
    .select("id, owner_id, title, due_date, reminder_sent")
    .not("due_date", "is", null)
    .eq("reminder_sent", false)
    .gte("due_date", now.toISOString())
    .lte("due_date", sevenDaysFromNow.toISOString())

  if (error) {
    console.error("Error querying action plans:", error)
    throw error
  }

  if (!plans || plans.length === 0) {
    console.log("No due notifications to send")
    return []
  }

  // Group by user_id
  const userNotifications = new Map<string, DueNotification>()

  for (const plan of plans) {
    if (!userNotifications.has(plan.owner_id)) {
      userNotifications.set(plan.owner_id, { user_id: plan.owner_id, plans: [] })
    }

    userNotifications.get(plan.owner_id)!.plans.push({
      title: plan.title,
      due_date: formatDate(plan.due_date),
      status: getPlanStatus(plan.due_date),
    })
  }

  return Array.from(userNotifications.values())
}

async function queryDueSchedules(supabase: any): Promise<ScheduleNotification[]> {
  const now = new Date()
  
  // Query schedules where:
  // 1. next_due is within reminder_days_before from now
  // 2. active = true
  const { data: schedules, error } = await supabase
    .from("evaluation_schedules")
    .select("id, name, next_due, reminder_days_before, created_by")
    .eq("active", true)

  if (error) {
    console.error("Error querying evaluation_schedules:", error)
    throw error
  }

  if (!schedules || schedules.length === 0) {
    console.log("No due schedules")
    return []
  }

  // Filter schedules that are due for reminder
  const dueSchedules: ScheduleNotification[] = []
  
  for (const schedule of schedules) {
    const nextDue = new Date(schedule.next_due)
    const reminderThreshold = new Date(now.getTime() + schedule.reminder_days_before * 24 * 60 * 60 * 1000)
    
    // Check if next_due is between now and reminder_days_before
    if (nextDue >= now && nextDue <= reminderThreshold) {
      dueSchedules.push({
        schedule_id: schedule.id,
        user_id: schedule.created_by,
        schedule_name: schedule.name,
        due_date: formatDate(schedule.next_due),
      })
    }
  }

  return dueSchedules
}

async function triggerSendEmail(supabase: any, userId: string, plans: any[], type: string = "action_plan_reminder", scheduleInfo?: any) {
  const sendEmailUrl = `${Deno.env.get("SUPABASE_URL")}/functions/v1/send-email`

  const payload: any = {
    type,
    user_id: userId,
    data: type === "schedule_reminder" ? { schedule: scheduleInfo } : { action_plans: plans },
  }

  const response = await fetch(sendEmailUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`,
    },
    body: JSON.stringify(payload),
  })

  return response.json()
}

async function markRemindersSent(supabase: any, planIds: string[]) {
  const { error } = await supabase
    .from("action_plans")
    .update({ reminder_sent: true })
    .in("id", planIds)

  if (error) {
    console.error("Error updating reminder_sent:", error)
    throw error
  }
}

async function updateScheduleNextDue(supabase: any, scheduleId: string, currentDue: string, frequency: string) {
  const nextDue = calculateNextDue(currentDue, frequency)
  
  const { error } = await supabase
    .from("evaluation_schedules")
    .update({ next_due: nextDue })
    .eq("id", scheduleId)

  if (error) {
    console.error("Error updating schedule next_due:", error)
    throw error
  }
  
  return nextDue
}

serve(async (req) => {
  // Handle CORS preflight (though cron doesn't typically need this)
  if (req.method === "OPTIONS") {
    return new Response("ok", {
      headers: {
        "Access-Control-Allow-Origin": "*",
      },
    })
  }

  try {
    console.log("Starting check-due-notifications cron job")

    const supabaseUrl = Deno.env.get("SUPABASE_URL")!
    const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!

    const supabase = createClient(supabaseUrl, supabaseServiceKey)

    // Process action plan reminders
    const notifications = await queryDueNotifications(supabase)
    console.log(`Found ${notifications.length} users with due action plan notifications`)

    let planSuccessCount = 0
    let planFailCount = 0

    for (const notification of notifications) {
      try {
        console.log(`Sending action plan reminder to user ${notification.user_id} with ${notification.plans.length} plans`)

        const result = await triggerSendEmail(supabase, notification.user_id, notification.plans)

        if (result.success) {
          planSuccessCount++
        } else {
          console.error(`Failed to send email to user ${notification.user_id}:`, result.error)
          planFailCount++
        }
      } catch (error) {
        console.error(`Error processing notification for user ${notification.user_id}:`, error)
        planFailCount++
      }
    }

    // Process evaluation schedule reminders
    const scheduleNotifications = await queryDueSchedules(supabase)
    console.log(`Found ${scheduleNotifications.length} schedules due for reminder`)

    let scheduleSuccessCount = 0
    let scheduleFailCount = 0

    for (const schedule of scheduleNotifications) {
      try {
        console.log(`Sending schedule reminder for "${schedule.schedule_name}" to user ${schedule.user_id}`)

        const result = await triggerSendEmail(
          supabase, 
          schedule.user_id, 
          [], 
          "schedule_reminder",
          {
            name: schedule.schedule_name,
            due_date: schedule.due_date,
          }
        )

        if (result.success) {
          scheduleSuccessCount++
          
          // Update next_due based on frequency
          // Get the frequency from the schedule first
          const { data: scheduleData } = await supabase
            .from("evaluation_schedules")
            .select("next_due, frequency")
            .eq("id", schedule.schedule_id)
            .single()
          
          if (scheduleData) {
            await updateScheduleNextDue(
              supabase, 
              schedule.schedule_id, 
              scheduleData.next_due, 
              scheduleData.frequency
            )
            console.log(`Updated schedule ${schedule.schedule_id} next_due`)
          }
        } else {
          console.error(`Failed to send schedule reminder for ${schedule.schedule_name}:`, result.error)
          scheduleFailCount++
        }
      } catch (error) {
        console.error(`Error processing schedule reminder for ${schedule.schedule_name}:`, error)
        scheduleFailCount++
      }
    }

    const totalSuccess = planSuccessCount + scheduleSuccessCount
    const totalFail = planFailCount + scheduleFailCount

    const message = `Processed action plans: ${planSuccessCount} sent, ${planFailCount} failed | Schedules: ${scheduleSuccessCount} sent, ${scheduleFailCount} failed`

    return new Response(JSON.stringify({
      success: true,
      message,
      details: {
        action_plans: {
          users_processed: notifications.length,
          success_count: planSuccessCount,
          fail_count: planFailCount,
        },
        schedules: {
          processed: scheduleNotifications.length,
          success_count: scheduleSuccessCount,
          fail_count: scheduleFailCount,
        },
      }
    }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    })

  } catch (error) {
    console.error("Error in check-due-notifications:", error)
    return new Response(JSON.stringify({
      success: false,
      error: String(error)
    }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    })
  }
})
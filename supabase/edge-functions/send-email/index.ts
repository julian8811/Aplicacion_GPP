// supabase/functions/send-email/index.ts
// HTTP function to send emails via Resend API
// Input: { type: "welcome" | "action_plan_reminder" | "weekly_summary", user_id: string, data?: object }

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"

const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY") || ""
const RESEND_FROM_EMAIL = Deno.env.get("RESEND_FROM_EMAIL") || "onboarding@resend.dev"

interface EmailRequest {
  type: "welcome" | "action_plan_reminder" | "weekly_summary"
  user_id: string
  data?: {
    name?: string
    establishment_name?: string
    action_plans?: Array<{ title: string; due_date: string; status: string }>
    stats?: {
      evaluations_completed: number
      pending_action_plans: number
      overdue_action_plans: number
    }
  }
}

async function getUserEmail(supabase: any, userId: string): Promise<string | null> {
  const { data, error } = await supabase
    .from("profiles")
    .select("email")
    .eq("id", userId)
    .single()

  if (error || !data?.email) {
    console.error("Could not fetch user email:", error)
    return null
  }
  return data.email
}

function buildWelcomeEmail(data: EmailRequest["data"]): { subject: string; html: string } {
  const name = data?.name || "Usuario"
  const establishmentName = data?.establishment_name || "GPP"

  return {
    subject: `Bienvenido a ${establishmentName}`,
    html: `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <style>
          body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }
          .content { background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }
          .button { display: inline-block; background: #667eea; color: white; padding: 12px 30px; border-radius: 6px; text-decoration: none; font-weight: 600; margin: 20px 0; }
          .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>¡Bienvenido, ${name}!</h1>
        </div>
        <div class="content">
          <p>Gracias por unirte a <strong>${establishmentName}</strong>. Estamos encantados de tenerte a bordo.</p>
          <p>Con nuestra herramienta podrás:</p>
          <ul>
            <li>Evaluar tus procesos operativos</li>
            <li>Crear planes de acción concretos</li>
            <li>Comparar tu rendimiento con estándares de la industria</li>
            <li>Generar informes profesionales en PDF</li>
          </ul>
          <p style="text-align: center;">
            <a href="#" class="button">Comenzar primera evaluación</a>
          </p>
          <p>Si tienes alguna pregunta, no dudes en contactarnos.</p>
          <p>Saludos,<br>El equipo de ${establishmentName}</p>
        </div>
        <div class="footer">
          Este email fue enviado porque te registraste en ${establishmentName}.
        </div>
      </body>
      </html>
    `,
  }
}

function buildActionPlanReminderEmail(data: EmailRequest["data"]): { subject: string; html: string } {
  const plans = data?.action_plans || []

  if (plans.length === 0) {
    return {
      subject: "Recordatorio: Planes de acción",
      html: "<p>No hay planes de acción pendientes.</p>",
    }
  }

  let plansTableRows = ""
  for (const plan of plans) {
    const statusColor = plan.status === "overdue" ? "#dc3545" : plan.status === "pending" ? "#ffc107" : "#28a745"
    plansTableRows += `
      <tr>
        <td style="padding: 12px; border-bottom: 1px solid #eee;">${plan.title}</td>
        <td style="padding: 12px; border-bottom: 1px solid #eee;">${plan.due_date}</td>
        <td style="padding: 12px; border-bottom: 1px solid #eee;">
          <span style="background: ${statusColor}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">${plan.status.toUpperCase()}</span>
        </td>
      </tr>
    `
  }

  return {
    subject: "Recordatorio: Planes de acción pendientes",
    html: `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <style>
          body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }
          .content { background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }
          table { width: 100%; border-collapse: collapse; margin: 20px 0; }
          th { background: #333; color: white; padding: 12px; text-align: left; }
          .button { display: inline-block; background: #f5576c; color: white; padding: 12px 30px; border-radius: 6px; text-decoration: none; font-weight: 600; margin: 20px 0; }
          .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>📋 Recordatorio de Planes de Acción</h1>
          <p>Tienes ${plans.length} plan(es) que requieren atención</p>
        </div>
        <div class="content">
          <table>
            <thead>
              <tr>
                <th>Plan</th>
                <th>Fecha Límite</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              ${plansTableRows}
            </tbody>
          </table>
          <p style="text-align: center;">
            <a href="#" class="button">Ver todos los planes</a>
          </p>
          <p>No dejes que tus tareas se acumulen. Revisa y actualiza el estado de tus planes de acción.</p>
        </div>
        <div class="footer">
          Este es un email automático. No respondas a este mensaje.
        </div>
      </body>
      </html>
    `,
  }
}

function buildWeeklySummaryEmail(data: EmailRequest["data"]): { subject: string; html: string } {
  const stats = data?.stats || { evaluations_completed: 0, pending_action_plans: 0, overdue_action_plans: 0 }

  return {
    subject: "Resumen Semanal - Tu actividad en GPP",
    html: `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <style>
          body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }
          .content { background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }
          .stats { display: flex; justify-content: space-around; margin: 20px 0; text-align: center; }
          .stat { flex: 1; }
          .stat-number { font-size: 2em; font-weight: bold; color: #4facfe; }
          .stat-label { color: #666; font-size: 14px; }
          .button { display: inline-block; background: #4facfe; color: white; padding: 12px 30px; border-radius: 6px; text-decoration: none; font-weight: 600; margin: 20px 0; }
          .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>📊 Tu Resumen Semanal</h1>
          <p>Así fue tu actividad esta semana</p>
        </div>
        <div class="content">
          <div class="stats">
            <div class="stat">
              <div class="stat-number">${stats.evaluations_completed}</div>
              <div class="stat-label">Evaluaciones completadas</div>
            </div>
            <div class="stat">
              <div class="stat-number">${stats.pending_action_plans}</div>
              <div class="stat-label">Planes pendientes</div>
            </div>
            <div class="stat">
              <div class="stat-number" style="color: #dc3545;">${stats.overdue_action_plans}</div>
              <div class="stat-label">Planes vencidos</div>
            </div>
          </div>
          <p style="text-align: center;">
            <a href="#" class="button">Ver dashboard</a>
          </p>
          <p>¡Sigue así! La evaluación constante de tus procesos es clave para la mejora continua.</p>
        </div>
        <div class="footer">
          Para dejar de recibir estos emails, actualiza tu configuración de notificaciones.
        </div>
      </body>
      </html>
    `,
  }
}

async function sendEmailViaResend(to: string, subject: string, html: string): Promise<{ success: boolean; message_id?: string; error?: string }> {
  if (!RESEND_API_KEY) {
    console.log(`[TEST MODE] Would send email to ${to}: ${subject}`)
    return { success: true, message_id: "test_mode_no_send" }
  }

  try {
    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${RESEND_API_KEY}`,
      },
      body: JSON.stringify({
        from: RESEND_FROM_EMAIL,
        to: to,
        subject: subject,
        html: html,
      }),
    })

    if (!response.ok) {
      const error = await response.text()
      console.error("Resend API error:", error)
      return { success: false, error }
    }

    const result = await response.json()
    console.log("Email sent successfully:", result)
    return { success: true, message_id: result.id }
  } catch (error) {
    console.error("Failed to send email:", error)
    return { success: false, error: String(error) }
  }
}

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
      },
    })
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!
    const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!

    const supabase = createClient(supabaseUrl, supabaseServiceKey)

    const { type, user_id, data }: EmailRequest = await req.json()

    if (!type || !user_id) {
      return new Response(JSON.stringify({ error: "Missing required fields: type, user_id" }), {
        status: 400,
        headers: { "Content-Type": "application/json" },
      })
    }

    // Get user email from profiles table
    const userEmail = await getUserEmail(supabase, user_id)
    if (!userEmail) {
      return new Response(JSON.stringify({ error: "User email not found" }), {
        status: 404,
        headers: { "Content-Type": "application/json" },
      })
    }

    let emailContent: { subject: string; html: string }

    switch (type) {
      case "welcome":
        emailContent = buildWelcomeEmail(data)
        break
      case "action_plan_reminder":
        emailContent = buildActionPlanReminderEmail(data)
        break
      case "weekly_summary":
        emailContent = buildWeeklySummaryEmail(data)
        break
      default:
        return new Response(JSON.stringify({ error: `Unknown email type: ${type}` }), {
          status: 400,
          headers: { "Content-Type": "application/json" },
        })
    }

    const result = await sendEmailViaResend(userEmail, emailContent.subject, emailContent.html)

    return new Response(JSON.stringify(result), {
      status: result.success ? 200 : 500,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    })
  } catch (error) {
    console.error("Error in send-email function:", error)
    return new Response(JSON.stringify({ error: String(error) }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    })
  }
})
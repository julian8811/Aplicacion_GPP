# Settings Specification

## Purpose

User profile management, establishment details, theme toggle, and invitation system for owners to invite viewers by email.

## Requirements

### Requirement: View Profile

The system SHALL display the current user's profile: full_name, email, role (owner/viewer), establishment_name, and member since date.

#### Scenario: View profile settings

- GIVEN the user navigates to `/settings`
- WHEN the page loads
- THEN the system SHALL display all profile fields in read-only display mode

### Requirement: Edit Profile

The system SHALL allow users to update their `full_name` and `establishment_name`. Email and role SHALL NOT be editable by the user.

#### Scenario: Update establishment name

- GIVEN the user is on the settings page
- WHEN the user updates the establishment name and clicks "Save"
- THEN the system SHALL persist the change to `profiles.establishment_name`
- AND display "Profile updated" toast

### Requirement: Theme Toggle

The system SHALL allow users to toggle between light and dark theme. Theme preference SHALL persist in localStorage and apply on page load without flash.

#### Scenario: Toggle dark mode

- GIVEN the user is on the settings page
- WHEN the user toggles the theme switch to dark
- THEN the system SHALL apply dark theme immediately
- AND save preference to localStorage

### Requirement: Invite Viewers (Owner Only)

Owners SHALL be able to invite viewers by entering an email address. The system SHALL send an invitation email via Supabase Edge Function. Invited users SHALL receive a role of `viewer`.

#### Scenario: Send invitation

- GIVEN the current user is an owner
- WHEN the user enters `viewer@example.com` and clicks "Send Invitation"
- THEN the system SHALL send an invitation email to `viewer@example.com`
- AND the invitee SHALL be created with role `viewer` upon signup

#### Scenario: Non-owner cannot invite

- GIVEN the current user is a viewer
- WHEN the user navigates to the invites section
- THEN the system SHALL display "Owners only" and hide the invite form

### Requirement: Manage Invitations

Owners SHALL see a list of pending invitations and active viewers. Owners SHALL be able to revoke pending invitations.

#### Scenario: Revoke invitation

- GIVEN an owner has a pending invitation for `pending@example.com`
- WHEN the user clicks "Revoke" next to the invitation
- THEN the system SHALL cancel the pending invitation
- AND remove it from the invitations list
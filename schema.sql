-- ====================================================================
-- SMART CAMPUS MANAGEMENT SYSTEM - ALLIANCE UNIVERSITY
-- Emergency & Notification Management Database Schema
-- Run this in your Supabase Project: SQL Editor -> New Query -> Run
-- ====================================================================

-- 1. Create table for Campus Notifications
CREATE TABLE IF NOT EXISTS public.campus_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'announcement', -- 'emergency', 'announcement', 'security', 'medical', 'general'
    priority TEXT NOT NULL DEFAULT 'medium',        -- 'critical', 'high', 'medium', 'low'
    sender TEXT NOT NULL DEFAULT 'Campus Administration',
    location TEXT DEFAULT 'Campus-wide',
    is_emergency BOOLEAN DEFAULT FALSE,
    is_read BOOLEAN DEFAULT FALSE,
    status TEXT DEFAULT 'active',                   -- 'active', 'resolved', 'archived'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create table for Emergency Reports & SOS Alerts
CREATE TABLE IF NOT EXISTS public.emergency_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    contact_number TEXT NOT NULL,
    emergency_type TEXT NOT NULL,
    location TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'Critical',     -- 'Critical', 'High', 'Medium'
    description TEXT,
    status TEXT DEFAULT 'Active',                  -- 'Active', 'Dispatched', 'Resolved'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Enable Row-Level Security (RLS)
ALTER TABLE public.campus_notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.emergency_reports ENABLE ROW LEVEL SECURITY;

-- 4. Create Policies to allow read/write for the Prototype (Anon Public Access)
CREATE POLICY "Allow public read access to campus_notifications"
ON public.campus_notifications FOR SELECT
TO anon, authenticated
USING (true);

CREATE POLICY "Allow public insert to campus_notifications"
ON public.campus_notifications FOR INSERT
TO anon, authenticated
WITH CHECK (true);

CREATE POLICY "Allow public update to campus_notifications"
ON public.campus_notifications FOR UPDATE
TO anon, authenticated
USING (true);

CREATE POLICY "Allow public delete to campus_notifications"
ON public.campus_notifications FOR DELETE
TO anon, authenticated
USING (true);

-- Policies for emergency_reports
CREATE POLICY "Allow public read access to emergency_reports"
ON public.emergency_reports FOR SELECT
TO anon, authenticated
USING (true);

CREATE POLICY "Allow public insert to emergency_reports"
ON public.emergency_reports FOR INSERT
TO anon, authenticated
WITH CHECK (true);

CREATE POLICY "Allow public update to emergency_reports"
ON public.emergency_reports FOR UPDATE
TO anon, authenticated
USING (true);

-- 5. Insert Initial Sample Campus Notifications (Matching PPT Slides)
INSERT INTO public.campus_notifications (title, message, category, priority, sender, location, is_emergency, is_read, status, created_at)
VALUES 
    (
        'Seminar Announcement',
        'A technical seminar on Artificial Intelligence will be conducted in the Seminar Hall.',
        'announcement',
        'medium',
        'Department of Computer Science',
        'Seminar Hall',
        false,
        false,
        'active',
        NOW() - INTERVAL '2 hours'
    ),
    (
        'Library Timings Update',
        'The library will remain open until 8 PM today for semester exam preparation.',
        'announcement',
        'low',
        'Central Library',
        'Central Library',
        false,
        false,
        'active',
        NOW() - INTERVAL '5 hours'
    ),
    (
        'Campus Safety & First Aid Drill',
        'Annual campus safety inspection and first aid training session at Student Activity Centre.',
        'security',
        'medium',
        'Alliance Campus Security',
        'Student Activity Centre',
        false,
        true,
        'active',
        NOW() - INTERVAL '1 day'
    );


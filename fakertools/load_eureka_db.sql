-- Populate InsightTypes Table
SET IDENTITY_INSERT InsightTypes ON;
INSERT INTO InsightTypes (id, type_name, description) VALUES
(1, 'Descriptive', 'Provides a summary of historical data.'),
(2, 'Predictive', 'Identifies trends and forecasts future.'),
(3, 'Prescriptive', 'Suggests specific actions to take.');
SET IDENTITY_INSERT InsightTypes OFF;

-- Populate DataSources Table
SET IDENTITY_INSERT DataSources ON;
INSERT INTO DataSources (id, source_name, description) VALUES
(1, 'Claims Data', 'Historical claims submitted by members.'),
(2, 'Member Portal Usage', 'Behavioral data from member portal logins.'),
(3, 'Pharmacy Data', 'Prescription drug usage and adherence data.'),
(4, 'Demographic Data', 'Member age, gender, and location information.');
SET IDENTITY_INSERT DataSources OFF;

-- Populate Audiences Table
SET IDENTITY_INSERT Audiences ON;
INSERT INTO Audiences (id, audience_name, description) VALUES
(1, 'Individual Members', 'Insights specific to individual members.'),
(2, 'Member Cohorts', 'Insights based on group segmentation.'),
(3, 'Organization-Wide', 'Insights relevant to the entire organization.');
SET IDENTITY_INSERT Audiences OFF;

-- Populate Domains Table
SET IDENTITY_INSERT Domains ON;
INSERT INTO Domains (id, domain_name, description) VALUES
(1, 'Health Outcomes', 'Insights related to health improvement.'),
(2, 'Operational Efficiency', 'Reducing costs and improving workflows.'),
(3, 'Member Engagement', 'Driving better usage of member tools.');
SET IDENTITY_INSERT Domains OFF;

-- Populate Feedback Table
-- SET IDENTITY_INSERT Feedback ON;
-- INSERT INTO Feedback (id, insight_id, delivery_channel_id, engagement_metric, engagement_value, feedback_text, created_at) VALUES
-- (1, 1, 1, 'Click-Through Rate', 75.5, 'Positive response to targeted campaigns.', CURRENT_TIMESTAMP),
-- (2, 2, 2, 'Conversion Rate', 20.0, 'Campaign increased adherence rates slightly.', CURRENT_TIMESTAMP),
-- (3, 3, 3, 'Notification Open Rate', 40.0, 'Users opened notifications but did not engage further.', CURRENT_TIMESTAMP);
-- SET IDENTITY_INSERT Feedback OFF;
SET IDENTITY_INSERT AlignmentGoals ON;
INSERT INTO AlignmentGoals (id, goal_name, description) VALUES
(1, 'Cost Optimization', 'Focus on reducing operational and claims costs.'),
(2, 'Member Engagement', 'Improve member interaction with digital platforms.'),
(3, 'Risk Mitigation', 'Identify and mitigate health or financial risks.'),
(4, 'Health Improvement', 'Drive better health outcomes through preventive programs.'),
(5, 'Operational Efficiency', 'Streamline processes to improve workflow and reduce waste.');
SET IDENTITY_INSERT AlignmentGoals OFF;
-- Populate Timeliness Table
SET IDENTITY_INSERT Timeliness ON;
INSERT INTO Timeliness (id, timeliness_type, description) VALUES
(1, 'Real-Time', 'Insights generated in real-time for immediate action.'),
(2, 'Periodic', 'Insights generated at regular intervals (e.g., daily, weekly).'),
(3, 'Historical', 'Insights based on past data for trend analysis and forecasting.');
SET IDENTITY_INSERT Timeliness OFF;

-- Populate DeliveryChannels Table
SET IDENTITY_INSERT DeliveryChannels ON;
INSERT INTO DeliveryChannels (id, channel_name, description) VALUES
(1, 'Notifications', 'Deliver insights via push notifications to members.'),
(2, 'Email', 'Send insights or updates directly to users via email.'),
(3, 'Dashboards', 'Display insights on web-based or mobile dashboards.'),
(4, 'APIs', 'Deliver insights programmatically through APIs.'),
(5, 'SMS', 'Send insights or updates through text messages.');
SET IDENTITY_INSERT DeliveryChannels OFF;

-- Populate ConfidenceLevels Table
SET IDENTITY_INSERT ConfidenceLevels ON;
INSERT INTO ConfidenceLevels (id, level_name, description) VALUES
(1, 'High', 'Insights with strong data support and reliability.'),
(2, 'Medium', 'Insights with moderate confidence, requiring caution.'),
(3, 'Low', 'Insights with weak data support, used as suggestions.');
SET IDENTITY_INSERT ConfidenceLevels OFF;

-- Populate ValuePriorities Table
SET IDENTITY_INSERT ValuePriorities ON;
INSERT INTO ValuePriorities (id, priority_name, description) VALUES
(1, 'Actionable', 'Insights that require immediate attention or action.'),
(2, 'Informational', 'Insights intended for knowledge or awareness.'),
(3, 'Strategic', 'Insights designed for long-term planning or goals.');
SET IDENTITY_INSERT ValuePriorities OFF;


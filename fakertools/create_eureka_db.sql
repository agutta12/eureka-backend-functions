-- Switch to the eureka database
USE eureka;
-- Table: InsightTypes
CREATE TABLE InsightTypes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    type_name NVARCHAR(255) NOT NULL, -- Descriptive, Diagnostic, Predictive, Prescriptive
    description NVARCHAR(MAX)
);

-- Table: DataSources
CREATE TABLE DataSources (
    id INT IDENTITY(1,1) PRIMARY KEY,
    source_name NVARCHAR(255) NOT NULL, -- Claims, Behavioral, Demographics, etc.
    description NVARCHAR(MAX)
);

-- Table: Audiences
CREATE TABLE Audiences (
    id INT IDENTITY(1,1) PRIMARY KEY,
    audience_name NVARCHAR(255) NOT NULL, -- Member-specific, Cohort, Organization-wide
    description NVARCHAR(MAX)
);

-- Table: Domains
CREATE TABLE Domains (
    id INT IDENTITY(1,1) PRIMARY KEY,
    domain_name NVARCHAR(255) NOT NULL, -- Operational, Health, Engagement, Financial
    description NVARCHAR(MAX)
);

-- Table: ConfidenceLevels
CREATE TABLE ConfidenceLevels (
    id INT IDENTITY(1,1) PRIMARY KEY,
    level_name NVARCHAR(255) NOT NULL, -- High, Medium, Low
    description NVARCHAR(MAX)
);

-- Table: Timeliness
CREATE TABLE Timeliness (
    id INT IDENTITY(1,1) PRIMARY KEY,
    timeliness_type NVARCHAR(255) NOT NULL, -- Real-Time, Periodic, Historical
    description NVARCHAR(MAX)
);

-- Table: DeliveryChannels
CREATE TABLE DeliveryChannels (
    id INT IDENTITY(1,1) PRIMARY KEY,
    channel_name NVARCHAR(255) NOT NULL, -- Dashboards, Notifications, APIs
    description NVARCHAR(MAX)
);

-- Table: AlignmentGoals
CREATE TABLE AlignmentGoals (
    id INT IDENTITY(1,1) PRIMARY KEY,
    goal_name NVARCHAR(255) NOT NULL, -- Cost Optimization, Customer Experience
    description NVARCHAR(MAX)
);

-- Table: ValuePriorities
CREATE TABLE ValuePriorities (
    id INT IDENTITY(1,1) PRIMARY KEY,
    priority_name NVARCHAR(255) NOT NULL, -- Actionable, Informational, Strategic
    description NVARCHAR(MAX)
);

-- Table: Insights
CREATE TABLE Insights (
    id INT IDENTITY(1,1) PRIMARY KEY,
    insight_type_id INT NOT NULL, -- FK to InsightTypes
    data_source_id INT NOT NULL, -- FK to DataSources
    audience_id INT NOT NULL, -- FK to Audiences
    domain_id INT NOT NULL, -- FK to Domains
    confidence_level_id INT NOT NULL, -- FK to ConfidenceLevels
    timeliness_id INT NOT NULL, -- FK to Timeliness
    alignment_goal_id INT NOT NULL, -- FK to AlignmentGoals
    value_priority_id INT NOT NULL, -- FK to ValuePriorities
    content NVARCHAR(MAX) NOT NULL, -- Insight content
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (insight_type_id) REFERENCES InsightTypes (id),
    FOREIGN KEY (data_source_id) REFERENCES DataSources (id),
    FOREIGN KEY (audience_id) REFERENCES Audiences (id),
    FOREIGN KEY (domain_id) REFERENCES Domains (id),
    FOREIGN KEY (confidence_level_id) REFERENCES ConfidenceLevels (id),
    FOREIGN KEY (timeliness_id) REFERENCES Timeliness (id),
    FOREIGN KEY (alignment_goal_id) REFERENCES AlignmentGoals (id),
    FOREIGN KEY (value_priority_id) REFERENCES ValuePriorities (id)
);

-- Table: Feedback
CREATE TABLE Feedback (
    id INT IDENTITY(1,1) PRIMARY KEY,
    insight_id INT NOT NULL, -- FK to Insights
    delivery_channel_id INT NOT NULL, -- FK to DeliveryChannels
    engagement_metric NVARCHAR(255) NOT NULL, -- Click-through, Action-taken, etc.
    engagement_value FLOAT NOT NULL, -- Numerical value of the metric
    feedback_text NVARCHAR(MAX), -- Optional feedback text
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (insight_id) REFERENCES Insights (id),
    FOREIGN KEY (delivery_channel_id) REFERENCES DeliveryChannels (id)
);

CREATE TABLE Recommendations (
    id INT IDENTITY(1,1) PRIMARY KEY,
    insight_id INT NOT NULL,
    recommendation_text NVARCHAR(MAX) NOT NULL,
    confidence_level_id INT NOT NULL,
    delivery_channel_id INT NOT NULL,
    status NVARCHAR(255) DEFAULT 'Pending',
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (insight_id) REFERENCES Insights(id),
    FOREIGN KEY (confidence_level_id) REFERENCES ConfidenceLevels(id),
    FOREIGN KEY (delivery_channel_id) REFERENCES DeliveryChannels(id)
);

-- Indexes
CREATE INDEX IDX_recommendations_insight_id ON Recommendations(insight_id);
CREATE INDEX IDX_recommendations_status ON Recommendations(status);

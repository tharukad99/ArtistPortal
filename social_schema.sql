-- Social Analytics Module Tables for SQL Server

-- 1. Social Accounts (stores Meta tokens and linked Page/IG IDs)
CREATE TABLE SocialAccounts (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    ArtistId INT NOT NULL,
    Platform NVARCHAR(50) NOT NULL, -- 'meta'
    PageId NVARCHAR(100),
    IgBusinessId NVARCHAR(100),
    AccessToken NVARCHAR(MAX) NOT NULL,
    PageName NVARCHAR(200),
    IgHandle NVARCHAR(100),
    ExpiresAt DATETIME,
    LastSync DATETIME,
    CONSTRAINT FK_SocialAccounts_Artists FOREIGN KEY (ArtistId) REFERENCES Artists(ArtistId)
);

-- 2. Social Metrics (time-series storage for daily metrics)
CREATE TABLE SocialMetrics (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    ArtistId INT NOT NULL,
    Platform NVARCHAR(50) NOT NULL, -- 'facebook', 'instagram'
    MetricName NVARCHAR(100) NOT NULL, -- 'followers', 'reach', 'impressions', 'engagement'
    MetricDate DATE NOT NULL,
    Value BIGINT NOT NULL,
    DateCreated DATETIME DEFAULT GETUTCDATE(),
    CONSTRAINT FK_SocialMetrics_Artists FOREIGN KEY (ArtistId) REFERENCES Artists(ArtistId)
);

-- 3. Social Sync Logs (to track success/failure of API calls)
CREATE TABLE SocialSyncLogs (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    ArtistId INT NOT NULL,
    Platform NVARCHAR(50),
    RunTime DATETIME DEFAULT GETUTCDATE(),
    Status NVARCHAR(20), -- 'SUCCESS', 'ERROR'
    Message NVARCHAR(MAX),
    CONSTRAINT FK_SocialSyncLogs_Artists FOREIGN KEY (ArtistId) REFERENCES Artists(ArtistId)
);

-- Indexes for performance
CREATE INDEX IX_SocialMetrics_ArtistDate ON SocialMetrics (ArtistId, MetricDate);
CREATE INDEX IX_SocialMetrics_MetricName ON SocialMetrics (MetricName);
CREATE UNIQUE INDEX UIX_SocialMetrics_Uniqueness ON SocialMetrics (ArtistId, Platform, MetricName, MetricDate);

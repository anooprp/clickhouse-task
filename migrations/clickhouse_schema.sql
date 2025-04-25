CREATE TABLE IF NOT EXISTS advertiser
(
    id UInt32,
    name String,
    updated_at DateTime64(6),
    created_at DateTime64(6)
)
ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE IF NOT EXISTS campaign
(
    id UInt32,
    name String,
    bid Float64,
    budget Float64,
    start_date Date,
    end_date Date,
    advertiser_id UInt32,
    updated_at DateTime64(6),
    created_at DateTime64(6)
)
ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE IF NOT EXISTS impressions
(
    id UInt32,
    campaign_id UInt32,
    created_at DateTime64(6)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(created_at)
ORDER BY (campaign_id, created_at);

CREATE TABLE IF NOT EXISTS clicks
(
    id UInt32,
    campaign_id UInt32,
    created_at DateTime64(6)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(created_at)
ORDER BY (campaign_id, created_at);

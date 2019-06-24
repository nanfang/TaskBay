CREATE EXTENSION IF NOT EXISTS hstore;

CREATE TABLE task (
    id BIGSERIAL PRIMARY KEY,
    name VARCHCAR(1000) NOT NULL,
    state SMALLINT NOT NULL DEFAULT 0,
    start_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    added_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_update_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    retry_count SMALLINT NOT NULL DEFAULT 0,
    queue_name VARCHCAR(1000),
    machine VARCHCAR(1000),
    process_id INT,
    parent_task_id BIGINT
);

CREATE TABLE task_params (
    task_id BIGINT PRIMARY KEY,
    params HSTORE NOT NULL
);

CREATE TABLE task_logs (
    task_id BIGINT PRIMARY KEY,
    log TEXT
);


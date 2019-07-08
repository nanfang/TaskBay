-- TODO do I need to pick up some knowledge of CEP?
CREATE TABLE task_event (
    id BIGSERIAL PRIMARY KEY,
    task_id BIGINT NOT NULL,
    task_name VARCHCAR(1000) NOT NULL,
    event_name VARCHCAR(1000) NOT NULL,
    result VARCHCAR(2000) NOT NULL, -- only for completed event
    event_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    tag  VARCHCAR(1000)
)

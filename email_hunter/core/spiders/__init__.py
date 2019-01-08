PREPARE_STEPS = 2
PREPARE_STEP_WEIGHT = 4
EMAIL_PATTERNS_COUNT = 26
VALIDATION_STEPS_COUNT = 2


class TASK_STATES:
    pending = 'PENDING'
    in_progress = 'PROGRESS'
    failed = 'FAILED'
    done = 'COMPLETE'


def compute_cur_in_task_meta(meta):
    meta.update(current=meta['prepare']['cur'] * PREPARE_STEP_WEIGHT +\
            meta['candidates']['cur'] * VALIDATION_STEPS_COUNT * EMAIL_PATTERNS_COUNT +\
            meta['step']['cur'] * EMAIL_PATTERNS_COUNT + meta['pattern']['cur'])
    
    return meta
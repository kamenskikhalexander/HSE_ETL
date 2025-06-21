CREATE TABLE transactions_v2(
    msno String,
    payment_method_id Int32,
    payment_plan_days Int32,
    plan_list_price Int32,
    actual_amount_paid Int32,
    is_auto_renew Int8,
    transaction_date Utf8,
    membership_expire_date Utf8,
    is_cancel Int8,
    PRIMARY KEY (msno),
    INDEX `idx_transaction_date` GLOBAL ASYNC  ON (`transaction_date`),
    INDEX `idx_payment_method_id` GLOBAL ASYNC ON (`payment_method_id`) ,
    INDEX `idx_is_cancel` GLOBAL ASYNC ON (`is_cancel`)
);

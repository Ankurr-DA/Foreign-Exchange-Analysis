use sql_analytics2;

-- Checking for Missing Values in fx_rates
select 
sum(rate_id is null) as null_rate_id,
sum(date is null) as null_date,
sum(currency_pair is null) as null_currency_pair,
sum(exchange_rate is null) as null_exchange_rate
from fx_rates;

-- Checking for Missing Values in international_payments
select 
sum(payment_id is null) as null_payment_id,
sum(rate_id is null) as null_rate_id,
sum(sender_country is null) as null_sender_country,
sum(receiver_country is null) as null_receiver_country,
sum(amount_sent is null) as null_amount_sent,
sum(fee_charged is null) as null_fee_charged
from international_payments;

-- Checking for Missing Values in payment_status
select 
sum(payment_id is null) as null_payment_id,
sum(status is null) as null_status,
sum(delivery_time_hours is null) as null_delivery_time,
sum(failure_reason is null and lower(trim(status)) = 'failed') as null_failure_reason
from payment_status;

-- fx_rates table -----------------------------------
--  Auditing Messy Columns for Python Transformations
select date from fx_rates
where date not like '____-__-__';

--  Auditing Messy Columns for Python Transformations
select distinct currency_pair from fx_rates;

-- Identifing impossible values for Python Transformations
select exchange_rate from fx_rates 
where exchange_rate < 0;

-- international_payments table -----------------------------------
--  Auditing Messy Columns for Python Transformations
select distinct sender_country from international_payments;
select distinct receiver_country from international_payments;

-- Identifing impossible values for Python Transformations
select amount_sent from international_payments where amount_sent < 0;
select fee_charged from international_payments where fee_charged < 0;

-- payment status table -----------------------------------
--  Auditing Messy Columns for Python Transformations
select distinct status from payment_status;

-- Identifing impossible values for Python Transformations
select delivery_time_hours from payment_status where delivery_time_hours < 0;

-- Excluding duplicate records -----------------------------
create table fx_rates_clean select distinct * from fx_rates;
create table international_payments_clean select distinct * from international_payments;
create table payment_status_clean select distinct * from payment_status;

-- VIEW 1 ---------------------------------------------------
create view v_payment_rates as 
select i.payment_id, i.sender_country, i.receiver_country, i.amount_sent, i.fee_charged, 
f.currency_pair, f.exchange_rate, f.date from international_payments_clean i 
left join fx_rates_clean f on i.rate_id = f.rate_id;

-- VIEW 2 ----------------------------------------------------
create view v_delivery_status as
select i.payment_id, p.status, p.delivery_time_hours, p.failure_reason from international_payments_clean i 
left join payment_status_clean p on i.payment_id = p.payment_id;






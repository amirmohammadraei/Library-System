UPDATE `user_account` 
SET `date_created` = DATE_ADD(`date_created` , INTERVAL 1 DAY)
WHERE `userid` = 1;
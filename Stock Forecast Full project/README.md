# Stock Forecast Full project

In this project will be automated further the analysis made in folder Stock Forecast.

The model and the stock analyzed changed, the idea of this project is to create a full pipeline for trading with weekly reports.

The first step is see the result in unicredit_test notebook, which is the same analysis made in stock forecast folder.

Then we train model in unicredit_train.

Once saved the model and other useful transformers we are ready for daily prediction wit unicredit_daily_predict.

Then once a week you can run weekly_report to have a little statistical analysis of how the trading is going.

Note 1: weekly report in reality is not weekly because the file keeps updating with time so after 4 weeks would be a monthly report

Note 2: the trade is still manual

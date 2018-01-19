# Shanghai Metro Status

## 介绍

每隔 2 分钟会去请求下上海地铁官方 API 去获取地铁运行情况，如果出现异常的话会推送消息到 Telegram Channel [@shmetro_status](https://t.me/shmetro_status)

## 使用的服务

- AWS CloudWatch
- AWS Lambda
- [apex](http://apex.run/)

## 开发环境

- macOS 10.13.1
- Python3.6

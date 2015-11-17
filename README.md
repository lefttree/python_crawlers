# crawler for zhihu

## 知乎登录流程

- 首页获得`_xsrf`, 用户填用户名,密码, remember_me
- 然后一起post到`http://www.zhihu.com/login/email`
    + post form with above data
    + response是json
    + json里有验证码captcha

## crawler process

- get xsrf from "http://www.zhihu.com" response
- get 验证码
- 发射post
- 验证是否成功

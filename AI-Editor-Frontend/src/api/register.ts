import request from "@/utils/myrequest";

class RegisterAPI {
  /** 登录 接口*/
  static register(data: RegisterData) {
    const formData = new FormData();
    formData.append("username", data.username);
    formData.append("password", data.password);
    formData.append("role", data.password);
    // formData.append("captchaKey", data.captchaKey);
    // formData.append("captchaCode", data.captchaCode);
    return request<any, RegisterResult>({
      url: "/account/register",
      method: "post",
      data: formData,
    });
  }
}

export default RegisterAPI;

/** 登录请求参数 */
export interface RegisterData {
  /** 用户名 */
  username: string;
  /** 密码 */
  password: string;
  role: string;
  /** 验证码缓存key */
  // captchaKey: string;
  // /** 验证码 */
  // captchaCode: string;
}

/** 登录响应 */
export interface RegisterResult {
  /** 访问token */
  // accessToken?: string;
  // /** 过期时间(单位：毫秒) */
  // expires?: number;
  // /** 刷新token */
  // refreshToken?: string;
  // /** token 类型 */
  // tokenType?: string;
}

/** 验证码响应 */
export interface CaptchaResult {
  /** 验证码缓存key */
  captchaKey: string;
  /** 验证码图片Base64字符串 */
  captchaBase64: string;
}

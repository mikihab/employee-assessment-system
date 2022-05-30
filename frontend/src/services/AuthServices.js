import apis from "./Apis";
import { Get, Post } from "./axiosCall";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import React from "react";

class AuthService {
  constructor() {
    this.token = null;
    console.log(apis.BASE);
    console.log(apis.BASE_LOCAL_URL);
  }

  retriveToken = () => {
    return localStorage.getItem("Token");
  };

  storeToken = (t) => {
    localStorage.setItem("Token", t);
  };

  deleteToken = () => {
    localStorage.removeItem("Token");
  };

  LoginAuth = (u, p) => {
    var bodyFormData = new FormData();
    bodyFormData.append("username", u);
    bodyFormData.append("password", p);
    return Post({
      url: apis.LOGIN,
      data: bodyFormData,
    });
  };

  RequireToken = ({ children }) => {
    let location = useLocation();
    console.log(this.retriveToken);
    if (!this.retriveToken) {
      return <Link to="/" state={{ from: location }} />;
    }

    return children;
  };

  FetchAuth = (t) => {
    return Get({
      url: apis.GETDETAILSUSER,
      params: {
        Token: t,
      },
    });
  };
}

export default new AuthService();

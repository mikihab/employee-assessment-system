import { useLocation, Link } from "react-router-dom";
import React from "react";

export const setToken = (token) => {
  localStorage.setItem("madeuptoken", token);
};

export const fetchToken = (token) => {
  return localStorage.getItem("madeuptoken");
};

export const deleteToken = (token) => {
  return localStorage.removeItem("madeuptoken");
};

export function RequireToken({ children }) {
  let auth = fetchToken();
  let location = useLocation();

  if (!auth) {
    return <Link to="/" state={{ from: location }} />;
  }

  return children;
}

import React, { createContext, useContext, useState } from "react";
import isJWTValid from "../util/auth";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuth, setIsAuth] = useState(isJWTValid());

  const login = (token) => {
    localStorage.setItem("token", token);
    setIsAuth(true);
  };
  const logout = () => {
    localStorage.removeItem("token", token);
    setIsAuth(false);
  };


  return (
    <AuthContext.Provider value={{ isAuth, login, logout}}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

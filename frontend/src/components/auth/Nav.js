import React from "react";
import { Link } from "react-router-dom";

import "./Nav.css";
import BGNav from "../../assets/images/bg-nav.png";

export default function Nav() {
  const navStyle = {
    backgroundImage: `url(${BGNav})`,
    backgroundRepeat: "no-repeat",
    backgroundSize: "cover",
    backgroundPosition: "bottom",
  };
  return (
    <div className="Nav" style={navStyle}>
      <Link to="/">
        <div className="brand">
          <span className="logo">EAS</span>
          <span className="name">Employee Assessment System</span>
        </div>
      </Link>
    </div>
  );
}

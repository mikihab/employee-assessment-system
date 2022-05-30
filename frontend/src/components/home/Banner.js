import React from "react";
import { Link } from "react-router-dom";

import "./Banner.css";
import BelowIcon from "../../assets/icons/below.png";
import Avatar from "../../assets/icons/avatar.png";
import BGBanner from "../../assets/images/bg-banner.png";

export default function () {
  const bannerStyle = {
    backgroundImage: `url(${BGBanner})`,
    backgroundRepeat: "no-repeat",
    backgroundSize: "cover",
    backgroundPosition: "bottom",
  };

  return (
    <div className="Banner" style={bannerStyle}>
      <div className="menubar">
        <Link to="/">
          <div className="brand">
            <span className="logo">EAS</span>
            <span className="name">Employee Assessment System</span>
          </div>
        </Link>
        <div className="login">
          <Link to="login">
            <img src={Avatar} alt="sign in" />
            Sign in
          </Link>
        </div>
      </div>
      <div className="banner-container">
        <h1 className="head">Employee Assessment System</h1>
      </div>
      <div className="see-below">
        <img onClick={scrollDown} src={BelowIcon} alt="See below" />
      </div>
    </div>
  );
}

function scrollDown() {
  console.log("scroll");
  window.scroll(0, window.screen.availHeight);
}

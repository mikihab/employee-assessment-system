import React from "react";
import PropTypes from "prop-types";
import { useHistory } from "react-router-dom";
import "./UserLogin.css";
import { deleteToken } from "../../../services/Auth";
import Avatar from "../../../assets/icons/avatar.png";
import { Button } from "@chakra-ui/react";

export default function UserLogin(props) {
  let { fullname, avatarSrc } = props;
  const history = useHistory();
  const logoutHandler = () => {
    deleteToken();
    history.push("/");
  };

  return (
    <div className="UserLogin">
      <Button onClick={logoutHandler}>Sign out</Button>
      <img
        className="avatar"
        src={avatarSrc ? avatarSrc : Avatar}
        alt={fullname}
      />
      <span className="fullname">{fullname}</span>
    </div>
  );
}

UserLogin.propTypes = {
  fullname: PropTypes.string.isRequired,
  avatarSrc: PropTypes.string.isRequired,
};

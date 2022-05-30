import React from "react";
import { Link } from "react-router-dom";

import "./GoToBoard.css";

import ButtonPrimary from "../buttons/ButtonPrimary";

export default function GoToBoard() {
  return (
    <div className="GoToBoard">
      <div className="bottom-wrap">
        <div className="gtb student">
          <div className="title">Employee</div>
          <p>
            If you are an employee click the bellow button to access your
            dashboard.
          </p>
          <Link to="/dashboard/student">
            <ButtonPrimary handleClick={() => {}}>Atempt now</ButtonPrimary>
          </Link>
        </div>
        <div className="gtb teacher">
          <div className="title">Master</div>
          <p>
            If you are a master user click the bellow button to access your
            dashboard.
          </p>
          <Link to="/dashboard/teacher">
            <ButtonPrimary handleClick={() => {}}>Questioning</ButtonPrimary>
          </Link>
        </div>
      </div>
    </div>
  );
}

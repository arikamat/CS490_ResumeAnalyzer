import React from "react";
import ReactLoading from "react-loading";
import "./Loading.css";

const Loading = () => {
  return (
    <div className="loading-parent">
      <span className="loading-text">Loading...</span>
      <ReactLoading type="spin" color="white" height={50} width={50} />
    </div>
  );
};

export default Loading;

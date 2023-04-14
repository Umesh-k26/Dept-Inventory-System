import React from "react";

const Container = ({ children }) => {
  return (
    <div className="mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">{children}</div>
  );
};

export default Container;

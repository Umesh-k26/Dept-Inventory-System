import React from "react";
import { useState } from "react";
import DropDown from "components/Dropdown";

const AdminNav = ({ handleOptionClick, selectedOption }) => {
  const options = {
    user: [
      {
        id: 1,
        name: "Add User",
      },
      {
        id: 2,
        name: "Update User",
      },
      {
        id: 3,
        name: "Delete User",
      },
    ],
    asset: [
      {
        id: 11,
        name: "Add Asset",
      },
      {
        id: 22,
        name: "Update Asset",
      },
      {
        id: 33,
        name: "Delete Asset",
      },
    ],
    order: [
      {
        id: 111,
        name: "Add Order",
      },
      {
        id: 222,
        name: "Update Order",
      },
      {
        id: 333,
        name: "Delete Order",
      },
    ],
  };

  return (
    <>
      <div className="flex justify-start">
        <DropDown
          handleOptionClick={handleOptionClick}
          selectedOption={selectedOption}
          options={options.user}
          displayName={"User"}
        />
        <DropDown
          handleOptionClick={handleOptionClick}
          selectedOption={selectedOption}
          options={options.asset}
          displayName={"Asset"}
        />
        <DropDown
          handleOptionClick={handleOptionClick}
          selectedOption={selectedOption}
          options={options.order}
          displayName={"Order"}
        />
      </div>
    </>
  );
};

export default AdminNav;

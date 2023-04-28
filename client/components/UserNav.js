import React from "react";
import DropDown from "./Dropdown";

const UserNav = ({ handleOptionClick, selectedOption }) => {
  const options = {
    asset: [
      {
        id: 1,
        name: "Add Asset",
      },
      {
        id: 2,
        name: "Update Asset",
      },
      {
        id: 3,
        name: "Display Assets",
      },
      {
        id: 4, 
        name: "Assets Barcode",
      },
    ],
    bulkAsset: [
      {
        id: 11,
        name: "Add Bulk Asset",
      },
      {
        id: 22,
        name: "Update Bulk Asset",
      },
      {
        id: 33,
        name: "Display Bulk Assets",
      },
      {
        id: 44,
        name: "Bulk Assets Barcode"
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
        name: "Display Orders",
      },
    ],
  };
  return (
    <>
      <div className="flex justify-start">
        <DropDown
          handleOptionClick={handleOptionClick}
          selectedOption={selectedOption}
          options={options.asset}
          displayName={"Asset"}
        />
        <DropDown
          handleOptionClick={handleOptionClick}
          selectedOption={selectedOption}
          options={options.bulkAsset}
          displayName={"Bulk Asset"}
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

export default UserNav;

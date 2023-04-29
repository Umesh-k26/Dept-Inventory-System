import React from "react";
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
        name: "Activate/ Deactivate User",
      },
      {
        id: 4,
        name: "Display Users",
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
      {
        id: 44,
        name: "Display Assets",
      },
      {
        id: 55,
        name: "Assets Barcode"
      }
    ],
    bulkAsset: [
      {
        id: 111,
        name: "Add Bulk Asset",
      },
      {
        id: 222,
        name: "Update Bulk Asset",
      },
      {
        id: 333,
        name: "Delete Bulk Asset",
      },
      {
        id: 444,
        name: "Display Bulk Assets",
      },
      {
        id: 555,
        name: "Bulk Assets Barcode"
      },
    ],
    order: [
      {
        id: 1111,
        name: "Add Order",
      },
      {
        id: 2222,
        name: "Update Order",
      },
      {
        id: 3333,
        name: "Delete Order",
      },
      {
        id: 4444,
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

export default AdminNav;

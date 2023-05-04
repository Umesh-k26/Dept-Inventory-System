import React from "react";
import DropDown from "components/Dropdown";
import { useState } from "react";

const DisplayNav = ({ types }) => {
  const [selectedOption, setSelectedOption] = useState(null);

  const handleOptionClick = (option, callback) => {
    setSelectedOption(option);
    callback();
  };
  return (
    <>
      <div className="flex justify-start pt-10">
        {Object.entries(types).map(([key, value]) => {
          return (
            <DropDown
              key={key}
              handleOptionClick={handleOptionClick}
              selectedOption={selectedOption}
              options={value}
              displayName={key}
            />
          );
        })}
      </div>
      {Object.entries(types).map(([key, value]) => {
        return (
          <div key={key}>
            {value.map((option) => {
              if (option.id == selectedOption) {
                return <option.prop key={option.id} />;
              }
            })}
          </div>
        );
      })}
    </>
  );
};

export default DisplayNav;

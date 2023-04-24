import { useState } from "react";

const DropDown = ({
  handleOptionClick,
  selectedOption,
  options,
  displayName,
}) => {
  const toggleDropdown = () => setIsOpen(!isOpen);
  const [isOpen, setIsOpen] = useState(false);

  const callback = () => setIsOpen(false);
  return (
    <>
      <div className="flex flex-col w-full pb-10">
        <div className="relative inline-block text-left mx-auto">
          <div className="mx-auto">
            <button
              type="button"
              className="inline-flex justify-between w-auto px-4 py-2 text-sm font-medium text-white bg-gray-700 rounded-md hover:bg-gray-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75"
              id="options-menu"
              aria-haspopup="true"
              aria-expanded="true"
              onClick={toggleDropdown}
            >
              {displayName}
            </button>
          </div>

          <div
            className={`absolute mx-auto z-10 mt-2 w-auto rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 ${
              isOpen ? "" : "hidden"
            }`}
            aria-labelledby="options-menu"
            role="menu"
          >
            <div className="py-1 w-auto" role="none">
              {options?.map((option) => {
                return (
                  <button
                    key={option.id}
                    className={`${
                      selectedOption === option.id ? "bg-gray-200" : ""
                    } block w-auto px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:bg-gray-100 focus:text-gray-900`}
                    role="menuitem"
                    onClick={() => handleOptionClick(option.id, callback)}
                  >
                    {option.name}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
export default DropDown;

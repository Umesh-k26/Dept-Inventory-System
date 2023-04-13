import React, { useContext, useRef } from "react";
import Form from "components/Form";

export const AddUser = () => {
  const fields = [
    { type: "text", id: "user_id", required: true, label: "User Id" },
    { type: "text", id: "first_name", required: false, label: "First Name" },
    { type: "text", id: "last_name", required: false, label: "Last Name" },
    { type: "text", id: "gmail", required: true, label: "Email" },
    { type: "text", id: "user_type", required: true, label: "User Type" },
    { type: "text", id: "department", required: true, label: "Department" },
  ];
  const apiLink = "http://localhost:8000/add-user";
  return (
    <>
      <Form fields={fields} apiLink={apiLink} method={"POST"} />
    </>
  );
};

export const DeleteUser = () => {
  const fields = [
    { type: "text", id: "user_id", required: true, label: "User Id" },
  ];
  const apiLink = "http://localhost:8000/delete-user/${user_id}";

  return (
    <>
      <Form fields={fields} apiLink={apiLink} method={"DELETE"} />
    </>
  );
};
export const FilterUser = async () => {};

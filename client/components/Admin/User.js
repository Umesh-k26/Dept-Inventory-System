import React, { useContext, useRef } from "react";
import Form from "components/Form";
import DataTable from "components/Table"
import { apiBaseUrl } from "next-auth/client/_utils";

export const AddUser = () => {
  const fields = [
    { type: "text", id: "user_id", required: true, label: "User Id" },
    { type: "text", id: "first_name", required: false, label: "First Name" },
    { type: "text", id: "last_name", required: false, label: "Last Name" },
    { type: "text", id: "email", required: true, label: "Email" },
    {
      type: "select",
      id: "user_type",
      required: true,
      label: "User Type",
      options: [
        { value: "Student", label: "Student" },
        { value: "Faculty", label: "Faculty" },
        { value: "Staff", label: "Staff" },
        { value: "Admin", label: "Admin" },
      ],
    },
    { type: "text", id: "department", required: true, label: "Department" },
  ];
  const apiLink = "http://localhost:8000/add-user";
  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"POST"}
        submitName={"Add User"}
      />
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
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"DELETE"}
        submitName={"Delete User"}
      />
    </>
  );
};

export const UpdateUser = () => {
  const fields = [
    { type: "text", id: "user_id", required: true, label: "User Id" },
    { type: "text", id: "first_name", required: false, label: "First Name" },
    { type: "text", id: "last_name", required: false, label: "Last Name" },
    { type: "text", id: "email", required: false, label: "Email" },
    {
      type: "select",
      id: "user_type",
      required: false,
      label: "User Type",
      options: [
        { value: "Student", label: "Student" },
        { value: "Faculty", label: "Faculty" },
        { value: "Staff", label: "Staff" },
        { value: "Admin", label: "Admin" },
      ],
    },
    { type: "text", id: "department", required: false, label: "Department" },
  ];
  const apiLink = "http://localhost:8000/update-user";
  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"PUT"}
        submitName={"Update User"}
      />
    </>
  );
};

export const GetUsers = () => {
  const fields = [
    { type: "text", id: "user_id", required: true, label: "User Id" },
  ];
  const apiLink = "http://localhost:8000/get-user/${user_id}";

  return (
    <>
      <Form
        fields={fields}
        apiLink={apiLink}
        method={"GET"}
        submitName={"Get User"}
      />
    </>
  );
};

export const DisplayUsers = () => {
  const apiLink = "http://localhost:8000/get-all-user";

  return (
    <>
    <DataTable
      apiLink={apiLink}
      method={"GET"}
      tableName={"All Users"}
    />
    </>
  )
}

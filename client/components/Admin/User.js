import { getSession } from "next-auth/react";
import React, { useContext, useRef } from "react";

export const AddUser = () => {
  const baseURL = process.env.REACT_APP_API_BASEURL;
  console.log(baseURL);
  const userId = useRef(null);
  const firstName = useRef(null);
  const lastName = useRef(null);
  const email = useRef(null);
  const department = useRef(null);
  const userType = useRef(null);

  const addUser = async (event) => {
    event.preventDefault();

    const res = await fetch(`http://localhost:8000/add-user`, {
      method: "POST",
      body: JSON.stringify({
        user_id: userId.current.value,
        first_name: firstName.current.value,
        last_name: lastName.current.value,
        gmail: email.current.value,
        user_type: userType.current.value,
        department: department.current.value,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = res.json();
    console.log(data);
  };
  return (
    <>
      <div className="container flex">
        <form onSubmit={addUser}>
          <label htmlFor="user_id">User Id</label>
          <input type="text" id="user_id" ref={userId} required />
          <label htmlFor="first_name">First Name</label>
          <input type="text" id="first_name" ref={firstName} />
          <label htmlFor="last_name">Last Name</label>
          <input type="text" id="last_name" ref={lastName} />
          <label htmlFor="email">Email Id</label>
          <input type="text" id="email" ref={email} required />
          <label htmlFor="user_type">User Type</label>
          <input type="text" id="user_type" ref={userType} required />
          <label htmlFor="department">Department</label>
          <input type="text" id="department" ref={department} />
          <button type="submit">Add user</button>
        </form>
      </div>
    </>
  );
};

export const DeleteUser = () => {
  const userId = useRef(null);

  const deleteUser = async () => {
    const res = await fetch(`http://localhost:8000/${userId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
  };
  return (
    <>
      <div>
        <form onSubmit={deleteUser}>
          <label htmlFor="user_id">User Id</label>
          <input type="text" id="user_id" ref={userId} required />

          <button type="submit">Delete user</button>
        </form>
      </div>
    </>
  );
};
export const FilterUser = async () => {};

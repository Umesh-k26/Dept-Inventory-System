import Barcode from "react-barcode";
import React, { useRef, useState } from "react";
import { useSession } from "next-auth/react";
import Container from "./Container";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";


const FormField = ({ field }) => {
  const { id, type, required, label, accept, options } = field;

  switch (type) {
    case "text":
    case "email":
    case "url":
    case "password":
    case "number":
      return (
        <div>
          <label htmlFor={id} className="block text-gray-700 font-bold mb-2">
            {label}
            {required && <span className="text-red-500">*</span>}
          </label>
          <input
            type={type}
            id={id}
            name={id}
            required={required}
            step={field?.step}
            min={field?.min}
            max={field?.currentYear}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
      );
    case "tel":
    case "date":
    case "time":
    case "datetime-local":
      return (
        <div>
          <label htmlFor={id} className="block text-gray-700 font-bold mb-2">
            {label}
            {required && <span className="text-red-500">*</span>}
          </label>
          <input
            type={type}
            id={id}
            name={id}
            // ref={inputRefs[id]}
            required={required}
            min={field?.min}
            max={field?.currentYear}
            // placeholder={field?.currentYear}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
      );
    case "textarea":
      return (
        <div>
          <label htmlFor={id} className="block text-gray-700 font-bold mb-2">
            {label}
            {required && <span className="text-red-500">*</span>}
          </label>
          <textarea
            id={id}
            name={id}
            // ref={inputRefs[id]}
            required={required}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          ></textarea>
        </div>
      );
    case "select":
      return (
        <div>
          <label htmlFor={id} className="block text-gray-700 font-bold mb-2">
            {label}
            {required && <span className="text-red-500">*</span>}
          </label>
          <select
            id={id}
            name={id}
            // ref={inputRefs[id]}
            required={required}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:placeholder-gray-400  dark:focus:ring-blue-500 dark:focus:border-blue-500"
          >
            {options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      );
    case "checkbox":
      return (
        <div>
          <input
            type="checkbox"
            id={id}
            name={id}
            // ref={inputRefs[id]}
            required={required}
            className="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mr-2"
          />
          <label htmlFor={id} className="text-gray-700 font-bold">
            {label}
            {required && <span className="text-red-500">*</span>}
          </label>
        </div>
      );
    case "radio":
      return (
        <div>
          <label className="block text-gray-700 font-bold mb-2">{label}</label>
          {options.map((option) => (
            <div key={option.value} className="flex items-center">
              <input
                type="radio"
                id={option.id}
                name={id}
                // ref={inputRefs[option.id]}
                value={option.value}
                required={required}
                className="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mr-2"
              />
              <label htmlFor={option.id} className="text-gray-700 font">
                {}
              </label>
            </div>
          ))}
        </div>
      );
    case "file":
      return (
        <div>
          <label htmlFor={id} className="block text-gray-700 font-bold mb-2">
            {label}
            {required && <span className="text-red-500">*</span>}
          </label>
          <input
            type={type}
            id={id}
            name={id}
            accept={accept}
            // ref={inputRefs[id]}
            required={required}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
      );
    case "image":
      return (
        <div>
          <label htmlFor={id} className="block text-gray-700 font-bold mb-2">
            {label}
            {required && <span className="text-red-500">*</span>}
          </label>
          <input
            type="file"
            accept="image/*"
            id={id}
            name={id}
            // ref={inputRefs[id]}
            required={required}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
      );
    default:
      return null;
  }
};

export const BarcodeGenerator = ({
  fields,
  apiLink,
  method,
  submitName,
  headers,
}) => {
  const [barcodeValues, setBarcodeValues] = useState([]);
  const [assetDetails, setAssetDetails] = useState([]);
  const { data: session, status } = useSession();
  const [message, setMessage] = useState();
  const [loading, setLoading] = useState(false);
  const formRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(formRef.current);
    formData.forEach((value, key) => {
      if (value == "") formData[key] = null;
    });

    let reqBody = {};

    if (headers?.["Content-Type"] === "multipart/form-data") reqBody = formData;
    else formData.forEach((val, key) => (reqBody[key] = val));

    console.log(reqBody);
    for (let k in reqBody) {
      if (reqBody[k] == "") reqBody[k] = null;
    }
    try {
      let apiLinkWithParams = apiLink;
      // Replace placeholders in apiLink with corresponding form data
      Object.keys(reqBody).forEach((key) => {
        console.log(key);
        apiLinkWithParams = apiLinkWithParams.replace(
          `\${${key}}`,
          reqBody[key]
        );
      });
      console.log(apiLinkWithParams);
      console.log(headers);
      let reqHeaders = {};
      if (!headers) {
        reqBody = JSON.stringify(reqBody);
        reqHeaders = { "Content-Type": "application/json" };
      }
      const res = await fetch(apiLinkWithParams, {
        method: method,
        headers: {
          Authorization: session.accessToken,
          ...reqHeaders,
        },
        body: reqBody,
      });
      const data = await res.json();
      console.log(data);

      setBarcodeValues([]);
      setAssetDetails([])
      
      for (var i = 0; i < data[0].length; i++)
      {
        const s_no = data[0][i]
        const name = data[1][i]
        setBarcodeValues(oldArray => [...oldArray, s_no]);
        setAssetDetails(oldArray => [...oldArray, name])
      }    
      
      formRef.current.reset();
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <Container>
      <div className="mx-auto flex justify-center">
        <h1>{submitName}</h1>
      </div>
      <form
        ref={formRef}
        onSubmit={handleSubmit}
        className="shadow-md rounded px-8 pt-6 pb-8 mb-4 w-96 bg-slate-400 mx-auto  "
      >
        {fields.map((field) => (
          <FormField key={field.id} field={field} />
        ))}
        <div className="pt-6 w-32">
          {loading && (
            <Box sx={{ display: "flex" }}>
              <CircularProgress />
            </Box>
          )}
          {!loading && (
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            >
              {submitName}
            </button>
          )}
        </div>
      </form>
      <>
        {barcodeValues.map((barcodeValue, index) => (
          <div>
          <p>{assetDetails[index]}</p>
          <Barcode key={barcodeValue} value={barcodeValue} />
          </div>
        ))}
      </>
    </Container>
  );
};

export default BarcodeGenerator;

import Barcode from "react-barcode";
import React, { useRef, useState } from "react";
import { useSession } from "next-auth/react";
import Container from "./Container";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";
import { FormField } from 'components/Form'

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
          <div key={barcodeValue}>
          <p>{assetDetails[index]}</p>
          <Barcode  value={barcodeValue} />
          </div>
        ))}
      </>
    </Container>
  );
};


import { useRef } from "react";
import { useSession } from "next-auth/react";
import Container from "./Container";

// const FormField = ({ type, id, required, label, inputRef }) => {
//   return (
//     <div className="mb-4">
//       <label htmlFor={id} className="block text-gray-700 font-bold mb-2">
//         {label}
//         {required && <span className="text-red-500">*</span>}
//       </label>
//       <input
//         type={type}
//         id={id}
//         name={id}
//         required={required}
//         ref={inputRef}
//         className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
//       />
//     </div>
//   );
// };
const FormField = ({ field, inputRefs }) => {
  const { id, type, required, label, options } = field;

  switch (type) {
    case "text":
    case "email":
    case "url":
    case "password":
    case "number":
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
            ref={inputRefs[id]}
            required={required}
            min={field?.min}
            max={field?.max}
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
            ref={inputRefs[id]}
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
            ref={inputRefs[id]}
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
            ref={inputRefs[id]}
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
                ref={inputRefs[option.id]}
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
            ref={inputRefs[id]}
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
            ref={inputRefs[id]}
            required={required}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
      );
    default:
      return null;
  }
};

const Form = ({ fields, apiLink, method, submitName }) => {
  const { data: session, status } = useSession();
  const formRef = useRef(null);
  const inputRefs = fields.reduce((acc, field) => {
    acc[field.id] = useRef(null);
    return acc;
  }, {});

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = {};
    fields.forEach((field) => {
      if (field.type == "file") {
        const file = inputRefs[field.id].current.files[0];
        const fileData = new FormData();
        fileData.append("image", file);
        formData[field.id] = fileData;
      } else {
        formData[field.id] = inputRefs[field.id].current.value;
        if (inputRefs[field.id].current.value === "") formData[field.id] = null;
      }
      console.log(inputRefs[field.id].current);
    });
    // return;
    try {
      let apiLinkWithParams = apiLink;
      // Replace placeholders in apiLink with corresponding form data
      Object.keys(formData).forEach((key) => {
        apiLinkWithParams = apiLinkWithParams.replace(
          `\${${key}}`,
          formData[key]
        );
      });
      const res = await fetch(apiLinkWithParams, {
        method: method,
        headers: {
          Authorization: session.accessToken,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      console.log(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Container>
      <form
        ref={formRef}
        onSubmit={handleSubmit}
        className="shadow-md rounded px-8 pt-6 pb-8 mb-4 w-96 bg-slate-400"
      >
        {fields.map((field) => (
          <FormField key={field.id} field={field} inputRefs={inputRefs} />
        ))}
        <div className="pt-6">
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            {submitName}
          </button>
        </div>
      </form>
    </Container>
  );
};

export default Form;

import { useRef } from "react";
import { useSession } from "next-auth/react";

const FormField = ({ type, id, required, label, inputRef }) => {
  return (
    <div className="mb-4">
      <label htmlFor={id} className="block text-gray-700 font-bold mb-2">
        {label}
        {required && <span className="text-red-500">*</span>}
      </label>
      <input
        type={type}
        id={id}
        name={id}
        required={required}
        ref={inputRef}
        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      />
    </div>
  );
};

const Form = ({ fields, apiLink, method }) => {
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
      formData[field.id] = inputRefs[field.id].current.value;
    });
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
    <form ref={formRef} onSubmit={handleSubmit}>
      {fields.map((field) => (
        <FormField
          key={field.id}
          type={field.type}
          id={field.id}
          required={field.required}
          label={field.label}
          inputRef={inputRefs[field.id]}
        />
      ))}
      <button
        type="submit"
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Submit
      </button>
    </form>
  );
};

export default Form;

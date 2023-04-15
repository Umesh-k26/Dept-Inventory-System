import React, { useEffect, useState } from "react";
import { useSession } from "next-auth/react";
import MUIDataTable from "mui-datatables";
import Container from "./Container";
import PropTypes from "prop-types";

export function Table({ data }) {
  const headers = Object.keys(data[0]);

  return (
    <table className="table-auto w-full">
      <thead>
        <tr>
          {headers.map((header) => (
            <th key={header} className="px-4 py-2">
              {header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row) => (
          <tr key={row.id}>
            {headers.map((header) => (
              <td key={header} className="border px-4 py-2">
                {row[header]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

Table.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      // add more properties as needed, e.g.
      // name: PropTypes.string.isRequired,
      // age: PropTypes.number.isRequired,
    })
  ).isRequired,
};

const data = [
  ["John Doe", "johndoe@gmail.com", "Male", "25"],
  ["Jane Smith", "janesmith@gmail.com", "Female", "30"],
  ["Bob Johnson", "bobjohnson@gmail.com", "Male", "45"],
  ["Mary Davis", "marydavis@gmail.com", "Female", "32"],
];

// const columns = [
//   {
//     name: "Name",
//     options: {
//       filter: true,
//       sort: true,
//     },
//   },
//   {
//     name: "Email",
//     options: {
//       filter: true,
//       sort: true,
//     },
//   },
//   {
//     name: "Gender",
//     options: {
//       filter: true,
//       sort: true,
//     },
//   },
//   {
//     name: "Age",
//     options: {
//       filter: false,
//       sort: true,
//     },
//   },
// ];
const options = {
  filterType: "dropdown",
  download: true,
  print: true,
  selectableRows: "multiple",
  responsive: "vertical",
  selectableRows: "none",
  downloadOptions: {
    filterOptions: {
      useDisplayedColumnsOnly: true,
      useDisplayedRowsOnly: true,
    },
  },
};

export const DataTable = ({ apiLink, method }) => {
  const { data: session, status } = useSession();
  let columns = [];

  const [tableData, setTableData] = useState();

  useEffect(() => {
    const getData = async () => {
      const res = await fetch(apiLink, {
        method: method,
        headers: {
          // Authorization: session.accessToken,
          "Content-Type": "application/json",
        },
      });
      const json = await res.json();
      setTableData(json);
    };
    // fetch(apiLink, {
    //   method: method,
    //   headers: {
    //     // Authorization: session.accessToken,
    //       "Content-Type": "application/json",
    //   },
    // }).then(data => data.json()).then(tableData => setTableData(tableData))

    getData();
  }, []);

  if (tableData) {
    console.log(tableData)
    for (let i = 0; i < tableData.column_name.length; i++) {
      columns.push({
        name: tableData.column_name[i],
        options: {
          filter: false,
          sort: true,
        },
      });
    }

    return (
      <>
        <Container>
          <MUIDataTable
            data={tableData.values}
            columns={columns}
            options={options}
          />
        </Container>
      </>
    );
  }
};

export default DataTable;

import { useEffect, useState } from "react"
import Link from 'next/link'

function Home() {
  const [name, setName] = useState('');
  const initValue = { person_name: '', person_age: null }
  const [person, setPerson] = useState(initValue);

  const getPerson = async () => {
    console.log("name = ", name)
    const res = await fetch(`http://localhost:8000/get-person/${name}`)
    const data = await res.json()
    console.log(data[0])
    setPerson(data[0])
  }
  // useEffect(() => {
  //   const getPersons = async () => {
  //     const res = await fetch('http://localhost:8000/get-person/umesh')
  //     const data = await res.json()
  //     setPerson(data[0])
  //   }
  //   getPersons();
  // }, [])
  return (
    <>
      <Link href={'/account'}>Account page</Link>
      <hr />
      <input type="text" value={name} onChange={e => setName(e.target.value)} />
      <button onClick={getPerson}>Get Details</button>
      {
        // person &&
        <div>
          <h2>Person name : {person?.person_name}</h2>
          <h2>Person age : {person?.person_age}</h2>
        </div>
      }

    </>
  )
}
export default Home

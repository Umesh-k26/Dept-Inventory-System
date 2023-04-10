import { getSession, signOut, useSession } from 'next-auth/react'
import React, { useEffect, useState } from 'react'
import Link from 'next/link';

const Account = () => {
  const { data: session, status } = useSession();
  const [email, setEmail] = useState();
  useEffect(() => {
    const getEmail = async () => {
      if (session) {
        const res = await fetch('http://localhost:8000/', {
          headers: {
            Authorization: session.accessToken,
            'Content-Type': 'application/json',
          }
        })
        const data = await res.json()
        setEmail(data["email"])
      }
    }
    getEmail()
  }, [session])

  if (status === 'authenticated') {
    return (
      <>
        <Link href={'/'}>Home page</Link>
        <h1 className='text-3xl font-bold underline'>Welcome {session.user.name}</h1>
        {
          email &&
          <h2>Email from backend : {email}</h2>
        }
        <button onClick={() => signOut()}>Sign Out</button>
      </>
    )
  }
  return (
    <>
      <div>You are not signed in</div>
    </>
  )
}

export default Account

export const getServerSideProps = async (context) => {
  const session = await getSession(context);
  if (!session) {
    return {
      redirect: {
        destination: '/login'
      }
    }
  }
  return {
    props: { session },
  }

}
import { useSession, signIn, signOut } from 'next-auth/react'
import Link from 'next/link'

const Login = () => {
  const { data: session } = useSession()

  if (session) {
    return (
      <>
        <Link href={'/account'}>Account</Link>
        <div>
          <p>Welcome, {session.user.email}</p>
          <img src={session.user.image} style={{ borderRadius: '50px' }} />
          <button onClick={() => signOut()}>Sign Out</button>
        </div>
      </>
    )
  }
  else {
    return (
      <>
        <div>You are not signed in</div>
        <button onClick={() => signIn()}>Sign In</button>
      </>
    )
  }
}

export default Login;
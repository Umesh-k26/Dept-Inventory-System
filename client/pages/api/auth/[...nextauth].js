import NextAuth from "next-auth/next";
import GoogleProvider from 'next-auth/providers/google'


export default NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    })
  ],
  callbacks: {
    async jwt({ token, user, account, profile }) {
      if (user) {
        token.id = user.id;
      }
      if (account) {
        token.accessToken = account.id_token;
      }
      return token;
    },
    async session({ session, token}) {
      session.user.id = token.id;
      session.accessToken = token.accessToken;
      return session;
    },
  },
})
import NextAuth from "next-auth/next";
import GoogleProvider from "next-auth/providers/google";
import { redirect } from "next/dist/server/api-utils";

export default NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
  ],
  pages: {
    signIn: "/",
  },
  session: "jwt",
  callbacks: {
    async jwt({ token, user, account, profile }) {
      if (user) {
        token.id = user.id;
      }
      if (account) {
        token.accessToken = account.id_token;
      }
      // console.log("from [...nexauth] : ", token)
      return token;
    },
    async session({ session, token }) {
      session.user.id = token.id;
      session.accessToken = token.accessToken;
      try {
        const res = await fetch("http://localhost:8000/get-role", {
          headers: {
            Authorization: session.accessToken,
          },
        });
        const data = await res.json();
        session.statuscode = res.status;
        if (!res.ok) {
          session.message = data.detail;
        }
        if (res.status != 404) session.loggedIn = true;
      } catch (err) {
        console.log(err);
      }
      return session;
    },
  },
  // jwt: process.env.JWT_SECRET,
});

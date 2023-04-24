import Link from "next/link";

const Footer = () => {
  return (
    <footer className="bg-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        <div className="flex flex-wrap justify-between">
          <div className="w-full md:w-1/3 lg:w-1/4 px-4 mb-8 md:mb-0">
            <h3 className="text-white font-bold mb-2">IIT Hyderabad</h3>
            <p className="text-gray-400">Department Inventory System</p>
          </div>
          <div className="w-full md:w-1/3 lg:w-1/4 px-4 mb-8 md:mb-0">
            <h3 className="text-white font-bold mb-2">Links</h3>
            <ul className="list-none">
              <li className="mb-2">
                <Link href="/" className="text-gray-400 hover:text-white">
                  Home
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/" className="text-gray-400 hover:text-white">
                  About
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/" className="text-gray-400 hover:text-white">
                  Contact
                </Link>
              </li>
            </ul>
          </div>
          <div className="w-full md:w-1/3 lg:w-1/4 px-4 mb-8 md:mb-0">
            <h3 className="text-white font-bold mb-2">Social Media</h3>
            <ul className="list-none">
              <li className="mb-2">
                <Link href="/" className="text-gray-400 hover:text-white">
                  Twitter
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/" className="text-gray-400 hover:text-white">
                  Facebook
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/" className="text-gray-400 hover:text-white">
                  Instagram
                </Link>
              </li>
            </ul>
          </div>
          <div className="w-full md:w-1/3 lg:w-1/4 px-4 mb-8 md:mb-0">
            <h3 className="text-white font-bold mb-2">Contact Us</h3>
            <ul className="list-none">
              <li className="mb-2">
                <Link href="/" className="text-gray-400 hover:text-white">
                  Email
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/" className="text-gray-400 hover:text-white">
                  Phone
                </Link>
              </li>
              <li className="mb-2">
                <Link href="/" className="text-gray-400 hover:text-white">
                  Address
                </Link>
              </li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-700 pt-8 pb-8">
          <p className="text-sm text-gray-400 text-center">
            &copy; {new Date().getFullYear()} IIT Hyderabad. All rights
            reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

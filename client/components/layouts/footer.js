const Footer = () => {
  return (
    <footer className="bg-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-wrap justify-between">
          <div className="w-full md:w-1/3 lg:w-1/4 px-4 mb-8 md:mb-0">
            <h3 className="text-white font-bold mb-2">Company Name</h3>
            <p className="text-gray-400">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed
              tristique, tellus sit amet finibus commodo, augue tellus malesuada
              lorem, in dapibus mi metus eget mi.
            </p>
          </div>
          <div className="w-full md:w-1/3 lg:w-1/4 px-4 mb-8 md:mb-0">
            <h3 className="text-white font-bold mb-2">Links</h3>
            <ul className="list-none">
              <li className="mb-2">
                <a href="/" className="text-gray-400 hover:text-white">
                  Home
                </a>
              </li>
              <li className="mb-2">
                <a href="/" className="text-gray-400 hover:text-white">
                  About
                </a>
              </li>
              <li className="mb-2">
                <a href="/" className="text-gray-400 hover:text-white">
                  Contact
                </a>
              </li>
            </ul>
          </div>
          <div className="w-full md:w-1/3 lg:w-1/4 px-4 mb-8 md:mb-0">
            <h3 className="text-white font-bold mb-2">Social Media</h3>
            <ul className="list-none">
              <li className="mb-2">
                <a href="/" className="text-gray-400 hover:text-white">
                  Twitter
                </a>
              </li>
              <li className="mb-2">
                <a href="/" className="text-gray-400 hover:text-white">
                  Facebook
                </a>
              </li>
              <li className="mb-2">
                <a href="/" className="text-gray-400 hover:text-white">
                  Instagram
                </a>
              </li>
            </ul>
          </div>
          <div className="w-full md:w-1/3 lg:w-1/4 px-4 mb-8 md:mb-0">
            <h3 className="text-white font-bold mb-2">Contact Us</h3>
            <ul className="list-none">
              <li className="mb-2">
                <a href="/" className="text-gray-400 hover:text-white">
                  Email
                </a>
              </li>
              <li className="mb-2">
                <a href="/" className="text-gray-400 hover:text-white">
                  Phone
                </a>
              </li>
              <li className="mb-2">
                <a href="/" className="text-gray-400 hover:text-white">
                  Address
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-700 pt-8 pb-8">
          <p className="text-sm text-gray-400 text-center">
            &copy; {new Date().getFullYear()} Company Name. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

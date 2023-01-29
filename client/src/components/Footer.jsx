import React, { Fragment } from 'react'
import '../styles/css/footer.css'

const Footer = () => {
  return (
    <Fragment>
        <div className="footer">
          <div className="footer-copyright">
            <p>copyright &copy; {(new Date().getFullYear())} | Cynthia Chelang'at</p>
          </div>
        </div>
    </Fragment>
  )
}

export default Footer
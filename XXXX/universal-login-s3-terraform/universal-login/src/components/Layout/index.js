import React from "react"
import * as S from "./styled"
import PropTypes from "prop-types"

const Layout = ({ children }) => {
  return (
    <S.MainBackground>
      <S.MainWrapper className="col-12 col-md-8 col-lg-5 col-xl-4">{children}</S.MainWrapper>
    </S.MainBackground>
  )
}

Layout.propTypes = {
  children: PropTypes.node.isRequired,
}

export default Layout

import React from "react"
import * as S from "./styled"

const LoadingFeatures = () => {
  return (
    <>
      <S.MainWrapper className="d-flex align-items-center flex-column bd-highlight mb-3">
        <div className="spinner-border" role="status" />
        <S.Message className="text-center">Loading feature toggles ⏳</S.Message>
      </S.MainWrapper>
    </>
  )
}

export default LoadingFeatures

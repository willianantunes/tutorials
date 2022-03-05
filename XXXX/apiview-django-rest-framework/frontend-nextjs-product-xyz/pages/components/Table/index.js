import React from "react"
import * as S from "./styled"

const Table = ({ keyValueObject }) => {
  return (
    <S.TableWithScroll className="table">
      <thead>
        <tr>
          <th>Key</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {keyValueObject &&
          Object.entries(keyValueObject).map(([key, value], index) => {
            return (
              <tr key={index}>
                <td>{key}</td>
                <td>{`${value}`}</td>
              </tr>
            )
          })}
      </tbody>
    </S.TableWithScroll>
  )
}

export default Table

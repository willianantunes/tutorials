require('spec_helper')

RSpec.describe(Auth0Tag) do
  let(:tokens) { Object.new }

  it 'should render head' do
    # Arrange
    tag_name = "auth0"
    input = ":head "
    allow(tokens).to(receive(:line_number))
    # Act
    tag_head = Auth0Tag.__send__(:new, tag_name, input, tokens)
    # Assert
    expect(tag_head.render(nil)).to(be_truthy)
  end

  it 'should render widget' do
    # Arrange
    tag_name = "auth0"
    input = ":widget "
    allow(tokens).to(receive(:line_number))
    # Act
    tag_widget = Auth0Tag.__send__(:new, tag_name, input, tokens)
    # Assert
    expect(tag_widget.render(nil)).to(be_truthy)
  end
end

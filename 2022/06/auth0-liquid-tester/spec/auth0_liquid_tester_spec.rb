require('spec_helper')

RSpec.describe(Auth0LiquidTester) do
  let(:request_path) { '/' }

  it 'should render index page' do
    get request_path

    expected_templates = [
      "Verification Email (using Link)",
      "Verification Email (using Code)",
      "Welcome Email",
      "Enroll in Multifactor Authentication",
      "Change Password",
      "Blocked Account Email",
      "Password Breach Alert",
      "Verification Code for Email MFA",
      "User Invitation",
      "Passwordless Email",
    ]

    expect(last_response.status).to(be(200))

    expected_templates.each do |name|
      expect(last_response.body).to(include(name))
    end
  end
end

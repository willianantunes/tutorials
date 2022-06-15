require('faker')
require('logger')
require('liquid')
require('sinatra/base')
require('sinatra/namespace')
require_relative('./tags')
require_relative('./sinatra_helpers')
require_relative('./email_controller')
require_relative('./new_universal_login_controller')

class Auth0LiquidTester < CustomSinatraBase
  get '/' do
    email_templates = [
      {
        'link' => '/verification-email-link',
        'title' => 'Verification Email (using Link)',
        'description' => 'This email will be sent whenever a user signs up or logs in for the first time.'
      },
      {
        'link' => '/verification-email-code',
        'title' => 'Verification Email (using Code)',
        'description' => "This email will be sent in scenarios where the user needs to prove they have access to the
            email on file for an account: (1) You have enabled the code-based email verification flow, and a user
            signs up or logs into the account for the first time. (2) You have enabled the Adaptive MFA policy and
            there is a low-confidence transaction for which account ownership must be verified."
      },
      {
        'link' => '/welcome-email',
        'title' => 'Welcome Email',
        'description' => "This email will be sent once the user verifies their email address.
            If the Verification Email is turned off, it will be sent when
            the user signs up or logs in for the first time."
      },
      {
        'link' => '/enroll-in-mfa',
        'title' => 'Enroll in Multifactor Authentication',
        'description' => 'This email will be sent when an admin sends a guardian enrollment email.'
      },
      {
        'link' => '/change-password',
        'title' => 'Change Password',
        'description' => "This email will be sent whenever a user requests a password change.
            The password will not be changed until the user follows the verification link in the email."
      },
      {
        'link' => '/blocked-account',
        'title' => 'Blocked Account Email',
        'description' => 'This email will be sent whenever a user is blocked due to suspicious login attempts.'
      },
      {
        'link' => '/password-breach-alert',
        'title' => 'Password Breach Alert',
        'description' => "This email will be sent whenever Auth0 detects that the user is trying to access
            the application using a password that has been leaked by a third party."
      },
      {
        'link' => '/verification-code-mfa',
        'title' => 'Verification Code for Email MFA',
        'description' => 'Will provide the MFA verification code to a user that is using a MFA email verifier.'
      },
      {
        'link' => '/user-invitation',
        'title' => 'User Invitation',
        'description' => 'This email will be sent whenever a user is invited to an organization or application.'
      },
      {
        'link' => '/passwordless-email',
        'title' => 'Passwordless Email',
        'description' => 'Will provide a code which the user can use to log in.'
      },
    ]
    nul_templates = [
      {
        'link' => '/nul-basic',
        'title' => 'Basic',
        'description' => 'This is the simplest template possible.'
      },
      {
        'link' => '/nul-box-image',
        'title' => 'Login box + image',
        'description' => 'The following template will show the login box to the left, and an image to the right only
          for the login/signup pages. The rest of the pages will look like the default ones.'
      },
      {
        'link' => '/nul-footers',
        'title' => 'Page footers',
        'description' => 'The template adds a gray footer with links to Privacy Policy and Terms of Services.'
      },
    ]
    liquid :index, locals: { emails: email_templates, nuls: nul_templates }
  end

  use EmailController
  use NewUniversalLoginController
end

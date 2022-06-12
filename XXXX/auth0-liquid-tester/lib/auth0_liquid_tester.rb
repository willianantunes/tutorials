require('faker')
require('liquid')
require('sinatra/base')
require('sinatra/namespace')

class Auth0LiquidTester < Sinatra::Base
  use Rack::CommonLogger

  configure :development do
    register Sinatra::Reloader
  end

  configure do
    set :views => Proc.new { File.join(File.expand_path("..", root), "views") }
  end

  get '/' do
    email_templates = [
      {
        "link" => "/verification-email-link",
        "title" => "Verification Email (using Link)",
        "description" => "This email will be sent whenever a user signs up or logs in for the first time."
      },
      {
        "link" => "/verification-email-code",
        "title" => "Verification Email (using Code)",
        "description" => "This email will be sent in scenarios where the user needs to prove they have access to the
            email on file for an account: (1) You have enabled the code-based email verification flow, and a user
            signs up or logs into the account for the first time. (2) You have enabled the Adaptive MFA policy and
            there is a low-confidence transaction for which account ownership must be verified."
      },
      {
        "link" => "/welcome-email",
        "title" => "Welcome Email",
        "description" => "This email will be sent once the user verifies their email address.
            If the Verification Email is turned off, it will be sent when
            the user signs up or logs in for the first time."
      },
      {
        "link" => "/enroll-in-mfa",
        "title" => "Enroll in Multifactor Authentication",
        "description" => "This email will be sent when an admin sends a guardian enrollment email."
      },
      {
        "link" => "/change-password",
        "title" => "Change Password",
        "description" => "This email will be sent whenever a user requests a password change.
            The password will not be changed until the user follows the verification link in the email."
      },
      {
        "link" => "/blocked-account",
        "title" => "Blocked Account Email",
        "description" => "This email will be sent whenever a user is blocked due to suspicious login attempts."
      },
      {
        "link" => "/password-breach-alert",
        "title" => "Password Breach Alert",
        "description" => "This email will be sent whenever Auth0 detects that the user is trying to access
            the application using a password that has been leaked by a third party."
      },
      {
        "link" => "/verification-code-mfa",
        "title" => "Verification Code for Email MFA",
        "description" => "Will provide the MFA verification code to a user that is using a MFA email verifier."
      },
      {
        "link" => "/user-invitation",
        "title" => "User Invitation",
        "description" => "This email will be sent whenever a user is invited to an organization or application."
      },
      {
        "link" => "/passwordless-email",
        "title" => "Passwordless Email",
        "description" => "Will provide a code which the user can use to log in."
      },
    ]
    liquid :index, locals: { emails: email_templates }
  end

  get '/verification-email-link' do
    user_details = { "email" => "jafar@willianantunes.com" }
    liquid_variables = {
      user: user_details,
      url: "https://www.willianantunes.com/",
      support_url: "https://github.com/willianantunes/tutorials",
    }

    liquid :verify_email, locals: liquid_variables
  end

  get '/verification-email-code' do
    liquid_variables = {
      code: "ACMEQWERTY",
      url: "https://www.willianantunes.com/",
      support_url: "https://github.com/willianantunes/tutorials",
    }

    liquid :verify_email_by_code, locals: liquid_variables
  end

  get '/welcome-email' do
    liquid_variables = { support_url: "https://github.com/willianantunes/tutorials", }

    liquid :welcome_email, locals: liquid_variables
  end

  get '/enroll-in-mfa' do
    liquid_variables = {
      link: "https://www.raveofphonetics.com/",
      support_url: "https://github.com/willianantunes/tutorials",
    }

    liquid :enrollment_email, locals: liquid_variables
  end

  get '/change-password' do
    liquid_variables = {
      url: "https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious",
      support_url: "https://github.com/willianantunes/tutorials",
    }

    liquid :reset_email, locals: liquid_variables
  end

  get '/blocked-account' do
    user_details = { "city" => "Maringá", "country" => "Brazil", "source_ip" => "192.168.0.1" }
    liquid_variables = {
      user: user_details,
      url: "https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious",
      support_url: "https://github.com/willianantunes/tutorials",
    }

    liquid :blocked_account, locals: liquid_variables
  end

  get '/password-breach-alert' do
    liquid_variables = {
      url: "https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious",
      support_url: "https://github.com/willianantunes/tutorials",
    }

    liquid :stolen_credentials, locals: liquid_variables
  end

  get '/verification-code-mfa' do
    liquid_variables = { code: "ACMEQWERTY", support_url: "https://github.com/willianantunes/tutorials", }

    liquid :mfa_oob_code, locals: liquid_variables
  end

  get '/user-invitation' do
    user_details = { "email" => "aladdin@willianantunes.com" }
    inviter_details = { "name" => "Jafar" }
    organization_details = { "display_name" => "XYZ Organization", "name" => "xyz" }
    liquid_variables = {
      user: user_details,
      inviter: inviter_details,
      organization: organization_details,
      friendly_name: "Antunes",
      url: "https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious",
      support_url: "https://github.com/willianantunes/tutorials",
    }

    liquid :user_invitation, locals: liquid_variables
  end

  get '/passwordless-email' do
    liquid_variables = { code: "ACMEQWERTY", support_url: "https://github.com/willianantunes/tutorials", }

    liquid :passwordless_email, locals: liquid_variables
  end
end

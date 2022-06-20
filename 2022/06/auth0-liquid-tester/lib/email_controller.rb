class EmailController < CustomSinatraBase
  get '/verification-email-link' do
    user_attributes = current_user_attributes

    user_additional_attributes = { 'email' => 'jafar@willianantunes.com', }
    user_attributes.merge!(user_additional_attributes)
    liquid_variables = {
      user: user_attributes,
      url: 'https://www.willianantunes.com/',
      support_url: 'https://github.com/willianantunes/tutorials',
    }

    liquid :verify_email, locals: liquid_variables
  end

  get '/verification-email-code' do
    user_attributes = current_user_attributes
    liquid_variables = {
      user: user_attributes,
      code: 'ACMEQWERTY',
      support_url: 'https://github.com/willianantunes/tutorials',
    }

    liquid :verify_email_by_code, locals: liquid_variables
  end

  get '/welcome-email' do
    user_attributes = current_user_attributes
    liquid_variables = { user: user_attributes, support_url: 'https://github.com/willianantunes/tutorials', }

    liquid :welcome_email, locals: liquid_variables
  end

  get '/enroll-in-mfa' do
    user_attributes = current_user_attributes
    liquid_variables = {
      user: user_attributes,
      link: 'https://www.raveofphonetics.com/',
      support_url: 'https://github.com/willianantunes/tutorials',
    }

    liquid :enrollment_email, locals: liquid_variables
  end

  get '/change-password' do
    user_attributes = current_user_attributes
    liquid_variables = {
      user: user_attributes,
      url: 'https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious',
      support_url: 'https://github.com/willianantunes/tutorials',
    }

    liquid :reset_email, locals: liquid_variables
  end

  get '/blocked-account' do
    user_attributes = current_user_attributes
    user_additional_attributes = { 'city' => 'Maringá', 'country' => 'Brazil', 'source_ip' => '192.168.0.1' }
    user_attributes.merge!(user_additional_attributes)
    liquid_variables = {
      user: user_attributes,
      url: 'https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious',
      support_url: 'https://github.com/willianantunes/tutorials',
    }

    liquid :blocked_account, locals: liquid_variables
  end

  get '/password-breach-alert' do
    user_attributes = current_user_attributes
    liquid_variables = {
      user: user_attributes,
      url: 'https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious',
      support_url: 'https://github.com/willianantunes/tutorials',
    }

    liquid :stolen_credentials, locals: liquid_variables
  end

  get '/verification-code-mfa' do
    user_attributes = current_user_attributes
    liquid_variables = { user: user_attributes, code: 'ACMEQWERTY', support_url: 'https://github.com/willianantunes/tutorials', }

    liquid :mfa_oob_code, locals: liquid_variables
  end

  get '/user-invitation' do
    user_attributes = current_user_attributes
    user_additional_attributes = { 'email' => 'aladdin@willianantunes.com' }
    user_attributes.merge!(user_additional_attributes)
    inviter_details = { 'name' => 'Jafar' }
    organization_details = { 'display_name' => 'XYZ Organization', 'name' => 'xyz' }
    liquid_variables = {
      user: user_attributes,
      inviter: inviter_details,
      organization: organization_details,
      friendly_name: 'Antunes',
      url: 'https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious',
      support_url: 'https://github.com/willianantunes/tutorials',
    }

    liquid :user_invitation, locals: liquid_variables
  end

  get '/passwordless-email' do
    user_attributes = current_user_attributes
    liquid_variables = {
      user: user_attributes,
      code: 'ACMEQWERTY',
      support_url: 'https://github.com/willianantunes/tutorials',
    }

    liquid :passwordless_email, locals: liquid_variables
  end
end

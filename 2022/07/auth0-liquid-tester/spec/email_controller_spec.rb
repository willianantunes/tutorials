require('spec_helper')

RSpec.describe(EmailController) do
  context "verification email link" do
    it 'should render properly' do
      get '/verification-email-link'

      expected_values = [
        "jafar@willianantunes.com",
        "https://www.willianantunes.com/",
        "https://github.com/willianantunes/tutorials"
      ]

      expect(last_response.status).to(be(200))

      expected_values.each do |name|
        expect(last_response.body).to(include(name))
      end
    end
  end

  context "verification email code" do
    it 'should render properly' do
      get '/verification-email-code'

      expected_values = ["ACMEQWERTY", "https://github.com/willianantunes/tutorials"]

      expect(last_response.status).to(be(200))

      expected_values.each do |name|
        expect(last_response.body).to(include(name))
      end
    end
  end

  context "welcome email" do
    it 'should render properly' do
      get '/welcome-email'

      expected_values = ["https://github.com/willianantunes/tutorials"]

      expect(last_response.status).to(be(200))

      expected_values.each do |name|
        expect(last_response.body).to(include(name))
      end
    end
  end

  context "enroll in mfa email" do
    it 'should render properly' do
      get '/enroll-in-mfa'

      expected_values = ["https://www.raveofphonetics.com/", "https://github.com/willianantunes/tutorials",]

      expect(last_response.status).to(be(200))

      expected_values.each do |name|
        expect(last_response.body).to(include(name))
      end
    end
  end

  context "change password email" do
    it 'should render properly' do
      get '/change-password'

      expected_values = [
        "https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious",
        "https://github.com/willianantunes/tutorials",
      ]

      expect(last_response.status).to(be(200))

      expected_values.each do |name|
        expect(last_response.body).to(include(name))
      end
    end
  end

  context "blocked account email" do
    it 'should render properly' do
      get '/blocked-account'

      expected_values = [
        "Maringá",
        "Brazil",
        "192.168.0.1",
        "https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious",
        "https://github.com/willianantunes/tutorials",
      ]

      expect(last_response.status).to(be(200))

      expected_values.each do |name|
        expect(last_response.body).to(include(name))
      end
    end
  end

  context "password breach alert email" do
    it 'should render properly' do
      get '/password-breach-alert'

      expected_values = [
        "https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious",
        "https://github.com/willianantunes/tutorials",
      ]

      expect(last_response.status).to(be(200))

      expected_values.each do |name|
        expect(last_response.body).to(include(name))
      end
    end
  end

  context "verification code mfa email" do
    it 'should render properly' do
      get '/verification-code-mfa'

      expected_values = ["ACMEQWERTY", "https://github.com/willianantunes/tutorials",]

      expect(last_response.status).to(be(200))

      expected_values.each do |name|
        expect(last_response.body).to(include(name))
      end
    end
  end

  context "user invitation email" do
    it 'should render properly' do
      get '/user-invitation'

      expected_values = [
        "aladdin@willianantunes.com",
        "Jafar",
        "XYZ Organization",
        "xyz",
        "Antunes",
        "https://www.raveofphonetics.com?language=en-us&show-phonetic=0&show-punctuations=1&show-stress=1&show-syllables=1&text=You%20are%20rather%20curious",
        "https://github.com/willianantunes/tutorials",
      ]

      expect(last_response.status).to(be(200))

      expected_values.each do |name|
        expect(last_response.body).to(include(name))
      end
    end
  end

  context "passwordless email" do
    it 'should render properly' do
      get '/passwordless-email'

      expected_values = ["ACMEQWERTY", "https://github.com/willianantunes/tutorials",]

      expect(last_response.status).to(be(200))

      expected_values.each do |name|
        expect(last_response.body).to(include(name))
      end
    end
  end
end

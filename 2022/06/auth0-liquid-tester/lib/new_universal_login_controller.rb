class NewUniversalLoginController < CustomSinatraBase
  get '/nul-basic' do
    liquid_variables = { locale: "en", }

    liquid :new_universal_login_basic, locals: liquid_variables
  end

  get '/nul-box-image' do
    name = params[:promptName]
    name = if name then name else "login" end
    prompt_details = { 'name' => name }
    liquid_variables = { prompt: prompt_details, locale: "en", }

    liquid :new_universal_login_box_image, locals: liquid_variables
  end

  get '/nul-footers' do
    liquid_variables = { locale: "en", }

    liquid :new_universal_login_footers, locals: liquid_variables
  end

  get '/nul-terms-of-use' do
    name = params[:promptName]
    name = if name then name else "signup" end
    prompt_details = { 'name' => name }
    liquid_variables = { prompt: prompt_details, locale: "en", }

    liquid :new_universal_login_terms, locals: liquid_variables
  end
end
